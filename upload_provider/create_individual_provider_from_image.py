
from datetime import datetime
from models.db import db
from models.provider import IndividualProvider

def create_individual_provider_from_markdown(markdown_text: str, image_file) -> IndividualProvider:
    """
    Creates a new individual provider record from markdown text and image with placeholder values.
    Populates provider ID, markdown text, and image data with placeholder values for required fields.

    Args:
        markdown_text: The markdown text generated from the image
        image_file: The raw image file object from the form upload

    Returns:
        IndividualProvider: The newly created provider record
    """
    # Get next provider_id
    result = db.session.execute(db.text("SELECT nextval('individual_providers_provider_id_seq')"))
    next_id = result.scalar()

    # Create timestamp for the placeholder last name 
    current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    # Convert image to base64 for storage
    import base64
    image_bytes = None
    if image_file:
        image_bytes = base64.b64encode(image_file.read())

    # Create new provider with required placeholder values
    new_provider = IndividualProvider(
        npi="To be assigned",
        first_name="New Provider from Image",
        last_name=f"Created at {current_time}",
        provider_enrollment_form_markdown_text=markdown_text,
        provider_enrollment_form_image=image_bytes
    )

    # Add and commit to database
    db.session.add(new_provider)
    db.session.commit()

    return new_provider
