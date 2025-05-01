# WorkQueue · Design & Implementation Guide

## 1  Purpose
The **WorkQueue** module surfaces provider‑data issues (duplicates, missing attributes, validation flags) as actionable work items. Reviewers claim items, inspect the affected provider record, perform corrective actions, and then mark each item *resolved*.  This guide defines database schema, Flask routes, HTML templates, and UX patterns for the first release.

Below is a practical build-out plan that drops straight into your current structure and coding style. Everything is framed so you can copy/paste the pieces (or hand them to your coding agent) in the usual incremental commits.

⸻

1 — Data-model design

Column	Type	Notes
queue_id	Integer, PK	
provider_id	Integer, FK → individual_providers.provider_id	CASCADE on provider delete
issue_type	String(40)	enum‐ish: 'duplicate' · 'bad_npi' · 'missing_npi' · 'sanction' · …
description	Text	Auto-generate short default; editable
recommended_action	Text	Free-text (merge / remove / add data / other)
status	String(20)	'open' · 'in_progress' · 'resolved'
assigned_user_id	Integer, FK → users.id	NULL ⇒ unassigned
created_by_user_id	Integer, FK → users.id	who created the ticket
created_at	DateTime	default =utcnow()
updated_at	DateTime	auto-update via onupdate=utcnow()
resolved_at	DateTime	nullable

SQLAlchemy model (models/work_queue.py)

from .db import db
from datetime import datetime

class WorkQueueItem(db.Model):
    __tablename__ = "work_queue_items"

    queue_id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer,
                            db.ForeignKey("individual_providers.provider_id",
                                          ondelete="CASCADE"),
                            nullable=False)
    issue_type = db.Column(db.String(40), nullable=False)
    description = db.Column(db.Text, nullable=False)
    recommended_action = db.Column(db.Text)
    status = db.Column(db.String(20), default="open", nullable=False)
    assigned_user_id = db.Column(db.Integer,
                                 db.ForeignKey("users.id",
                                               ondelete="SET NULL"))
    created_by_user_id = db.Column(db.Integer,
                                   db.ForeignKey("users.id",
                                                 ondelete="SET NULL"))
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)

    # relationships
    provider = db.relationship("IndividualProvider")
    assigned_user = db.relationship("User",
                                    foreign_keys=[assigned_user_id])
    created_by_user = db.relationship("User",
                                      foreign_keys=[created_by_user_id])

Add WorkQueueItem to models/__init__.py export list.

Table DDL (add to create_tables.py)

CREATE TABLE IF NOT EXISTS work_queue_items (
    queue_id SERIAL PRIMARY KEY,
    provider_id INTEGER NOT NULL
        REFERENCES individual_providers(provider_id) ON DELETE CASCADE,
    issue_type TEXT NOT NULL,
    description TEXT NOT NULL,
    recommended_action TEXT,
    status TEXT NOT NULL DEFAULT 'open',
    assigned_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_by_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

⚡ Tip: When you switch to Alembic you can autogenerate this migration instead of editing create_tables.py.

⸻

2 — Blueprint & routes (work_queues/work_queue_routes.py)

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from main import db
from models import WorkQueueItem, IndividualProvider, User

wq_bp = Blueprint("work_queue", __name__,
                  template_folder="templates",
                  static_folder="static")

@wq_bp.route("/work_queue")
@login_required
def work_queue():
    items = WorkQueueItem.query.order_by(
        WorkQueueItem.status.desc(),  # open first
        WorkQueueItem.updated_at.desc()
    ).all()
    return render_template("work_queue.html", items=items)

@wq_bp.route("/work_queue/<int:queue_id>")
@login_required
def work_queue_item(queue_id):
    item = WorkQueueItem.query.get_or_404(queue_id)
    provider = item.provider
    return render_template("work_queue_item.html",
                           item=item, provider=provider)

@wq_bp.post("/work_queue/<int:queue_id>/update")
@login_required
def update_work_queue_item(queue_id):
    item = WorkQueueItem.query.get_or_404(queue_id)

    # editable fields
    item.recommended_action = request.form.get("recommended_action", "").strip()
    item.status = request.form.get("status", item.status)
    item.assigned_user_id = request.form.get("assigned_user_id") or None

    if item.status == "resolved" and not item.resolved_at:
        from datetime import datetime
        item.resolved_at = datetime.utcnow()

    db.session.commit()
    flash("Work-queue item updated", "success")
    return redirect(url_for("work_queue.work_queue_item", queue_id=queue_id))

@wq_bp.post("/work_queue/<int:queue_id>/assign_to_me")
@login_required
def assign_to_me(queue_id):
    item = WorkQueueItem.query.get_or_404(queue_id)
    item.assigned_user_id = current_user.id
    item.status = "in_progress"
    db.session.commit()
    flash("You are now assigned", "success")
    return redirect(url_for("work_queue.work_queue_item", queue_id=queue_id))

Register in main.py:

from work_queues.work_queue_routes import wq_bp
app.register_blueprint(wq_bp)



⸻

3 — Templates (Tailwind, minimal skeleton)

work_queue.html

{% extends "header.html" %}
{% block content %}
<div class="py-8 px-5">
  <h2 class="text-2xl font-bold mb-4">Work Queue</h2>

  <table class="min-w-full bg-white shadow rounded-lg">
    <thead class="bg-gray-50 text-xs uppercase tracking-wider text-gray-600">
      <tr>
        <th class="px-4 py-3">Provider</th>
        <th class="px-4 py-3">Issue</th>
        <th class="px-4 py-3">Status</th>
        <th class="px-4 py-3">Assigned</th>
        <th class="px-4 py-3">Updated</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-gray-200 text-sm">
      {% for item in items %}
      <tr class="hover:bg-gray-50">
        <td class="px-4 py-2">
          <a class="text-blue-600 hover:underline"
             href="{{ url_for('work_queue.work_queue_item', queue_id=item.queue_id) }}">
            {{ item.provider.first_name }} {{ item.provider.last_name }}
          </a>
        </td>
        <td class="px-4 py-2">{{ item.issue_type.replace('_', ' ').title() }}</td>
        <td class="px-4 py-2">{{ item.status }}</td>
        <td class="px-4 py-2">{{ item.assigned_user.email if item.assigned_user else '—' }}</td>
        <td class="px-4 py-2">{{ item.updated_at.strftime('%Y-%m-%d') }}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}

work_queue_item.html

{% extends "header.html" %}
{% block content %}
<div class="py-8 px-5 max-w-5xl mx-auto">
  <h2 class="text-2xl font-bold mb-2">Work Item #{{ item.queue_id }}</h2>
  <p class="text-gray-600 mb-6">Issue: <span class="font-medium">{{ item.issue_type }}</span></p>

  <!-- Provider snapshot (reuse existing styling) -->
  {% include "individual_provider_detail.html" with context %}

  <form method="POST"
        action="{{ url_for('work_queue.update_work_queue_item', queue_id=item.queue_id) }}"
        class="bg-white shadow rounded-lg p-6 mt-8 space-y-4">
    <div>
      <label class="block text-sm font-semibold text-gray-700 mb-1">Recommended action</label>
      <textarea name="recommended_action"
                class="w-full border rounded-md p-2"
                rows="3">{{ item.recommended_action or '' }}</textarea>
    </div>

    <div class="grid grid-cols-3 gap-4">
      <div>
        <label class="block text-sm font-semibold text-gray-700 mb-1">Status</label>
        <select name="status" class="w-full border rounded-md p-2">
          {% for s in ["open", "in_progress", "resolved"] %}
          <option value="{{ s }}" {% if item.status==s %}selected{% endif %}>{{ s|title }}</option>
          {% endfor %}
        </select>
      </div>

      <div>
        <label class="block text-sm font-semibold text-gray-700 mb-1">Assigned user</label>
        <select name="assigned_user_id" class="w-full border rounded-md p-2">
          <option value="">— Unassigned —</option>
          {% for u in users %}
          <option value="{{ u.id }}" {% if item.assigned_user_id==u.id %}selected{% endif %}>
            {{ u.email }}
          </option>
          {% endfor %}
        </select>
      </div>

      <div class="flex items-end">
        <button class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Save</button>
      </div>
    </div>
  </form>
</div>
{% endblock %}

Template data: Pass the users list from the route (User.query.order_by(User.email)).

⸻

4 — Front-end JS (optional niceties)
  •	work_queues/static/work_queue.js
  •	Add quick “Assign to me” button via fetch('/work_queue/<id>/assign_to_me', {method:'POST'}).
  •	Add <script> tag only on work_queue_item.html when logged-in user is shown.

⸻

5 — Navigation & RBAC
  1.	Header link

<a href="{{ url_for('work_queue.work_queue') }}" class="text-white hover:text-blue-200">🗂️ Queue</a>


  2.	Permissions
  •	For now you gate all routes with @login_required.
  •	Later you can add role checks (current_user.role in ('admin', 'data_steward')).

⸻

6 — Seeding sample tickets (insert_sample_data.py)

queue_items = [
    (1, 1, 'duplicate',
     'Possible duplicate of provider_id 2 (name & NPI similar)', None, 'open', None, 1),
    (2, 3, 'bad_npi',
     'NPI is 9 digits; should be 10', None, 'open', None, 1),
]
for qi in queue_items:
    cur.execute("""
        INSERT INTO work_queue_items
        (queue_id, provider_id, issue_type, description, recommended_action,
         status, assigned_user_id, created_by_user_id)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (queue_id) DO NOTHING
    """, qi)



⸻

7 — Implementation sequence

Step	Commit message
1	feat(db): add work_queue_items table & model
2	feat(app): blueprint + routes for work queue
3	feat(ui): list & detail templates with Tailwind
4	feat(nav): add Work Q link to header
5	chore(seed): sample tickets for demo
6	docs: README update – work-queue usage

Deploy after step 3 to test CRUD end-to-end, then polish.

⸻

Done — you now have a clear, slice-by-slice roadmap.

Let me know which piece you’d like fleshed out first or if you want tailored prompts for your coding agent (Py, SQL, or Tailwind snippets).