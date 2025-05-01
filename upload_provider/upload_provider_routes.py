"""
Blueprint: /upload
Purpose   : Image OCR → markdown, provider creation, data extraction,
            and conversion to Facets – all API endpoints return JSON.

Changes   : • Every route now returns JSON via `flask.jsonify`
            • Added blueprint-level error handler so any unhandled
              exception is returned as JSON instead of an HTML page
"""

from flask import (
    Blueprint,
    render_template,
    request,
    current_app,
    jsonify
)

# ─── Local utilities (import lazily in routes where they’re used) ────
# from .image_to_markdown_gpt import image_to_markdown
# from .provider_to_facets      import convert_and_save_provider_facets
# from .facets_json_to_markdown import convert_facets_json_to_markdown
# from .markdown_to_individual_provider_gpt import markdown_to_individual_provider_gpt
# from .create_individual_provider_from_image import create_individual_provider_from_markdown

upload_provider_bp = Blueprint(
    "upload_provider",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/upload/static",
    url_prefix="/upload"
)

# ───────────────────────────── Error handling ────────────────────────────
@upload_provider_bp.errorhandler(Exception)
def _jsonify_errors(err):
    """Return all unhandled errors as JSON so the frontend never receives HTML."""
    current_app.logger.exception("Unhandled upload-provider error")
    return jsonify(success=False, error=str(err)), 500


# ───────────────────────────── UI page ───────────────────────────────────
@upload_provider_bp.get("/")
def upload():                       # GET  /upload/
    return render_template("upload_provider.html")


# ───────────────────────────── Image → Markdown ──────────────────────────
@upload_provider_bp.post("/process")
def process_image():                # POST /upload/process
    uploaded_file = request.files.get("image_file")
    if not uploaded_file:
        return jsonify(success=False, error="No file provided"), 400

    from .image_to_markdown_gpt import image_to_markdown
    markdown = image_to_markdown(uploaded_file)

    return jsonify(success=True, markdown=markdown)   # <── JSON only!


# ───────────────────────────── Extract Provider Info ─────────────────────
@upload_provider_bp.post("/extract_provider_info/<int:provider_id>")
def extract_provider_info(provider_id):
    from .markdown_to_individual_provider_gpt import markdown_to_individual_provider_gpt
    success = markdown_to_individual_provider_gpt(provider_id)
    return jsonify(success=bool(success))


# ───────────────────────────── Provider creation ─────────────────────────
@upload_provider_bp.post("/create_provider")
def create_provider():
    markdown_text = request.form.get("markdown_text")
    image_file    = request.files.get("image_file")

    if not markdown_text:
        return jsonify(success=False, error="No markdown text provided"), 400

    from .create_individual_provider_from_image import (
        create_individual_provider_from_markdown,
    )
    provider = create_individual_provider_from_markdown(markdown_text, image_file)

    if not provider:
        return jsonify(success=False, error="Provider creation failed"), 500

    return jsonify(success=True, provider_id=provider.provider_id)


# ───────────────────────────── Convert to Facets ─────────────────────────
@upload_provider_bp.post("/convert_to_facets/<int:provider_id>")
def convert_to_facets(provider_id):
    """
    1. Build Facets JSON & persist
    2. Generate human-readable markdown summary
    """
    from .provider_to_facets import convert_and_save_provider_facets
    facets_result = convert_and_save_provider_facets(provider_id)

    if facets_result.get("status") != "success":
        return jsonify(
            success=False,
            error="Failed to generate Facets JSON",
            details=facets_result.get("message"),
        ), 400

    from .facets_json_to_markdown import convert_facets_json_to_markdown
    markdown_result = convert_facets_json_to_markdown(provider_id)

    if markdown_result.get("status") != "success":
        return jsonify(
            success=False,
            error="Failed to generate Facets markdown",
            details=markdown_result.get("message"),
        ), 400

    return jsonify(success=True)