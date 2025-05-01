
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
    users = User.query.order_by(User.email).all()
    return render_template("work_queue_item.html",
                         item=item, provider=provider, users=users)

@wq_bp.route("/work_queue/<int:queue_id>/update", methods=['POST'])
@login_required
def update_work_queue_item(queue_id):
    item = WorkQueueItem.query.get_or_404(queue_id)

    # Update editable fields
    item.recommended_action = request.form.get("recommended_action", "").strip()
    item.status = request.form.get("status", item.status)
    item.assigned_user_id = request.form.get("assigned_user_id") or None

    if item.status == "resolved" and not item.resolved_at:
        from datetime import datetime
        item.resolved_at = datetime.utcnow()

    db.session.commit()
    flash("Work queue item updated", "success")
    return redirect(url_for("work_queue.work_queue_item", queue_id=queue_id))

@wq_bp.route("/work_queue/<int:queue_id>/assign_to_me", methods=['POST'])
@login_required
def assign_to_me(queue_id):
    item = WorkQueueItem.query.get_or_404(queue_id)
    item.assigned_user_id = current_user.id
    item.status = "in_progress"
    db.session.commit()
    flash("You are now assigned", "success")
    return redirect(url_for("work_queue.work_queue_item", queue_id=queue_id))
