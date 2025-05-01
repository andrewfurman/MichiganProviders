from flask import current_app, request, redirect, url_for, flash
from flask_login import current_user
from main import db
from models import IndividualProvider
from models.provider_audit import ProviderAudit
from models.auth import User
import logging
import traceback

logger = logging.getLogger(__name__)
logger.debug("Models imported: IndividualProvider, ProviderAudit, User")

def update_individual_provider(provider_id):
    logger = current_app.logger
    logger.setLevel(logging.DEBUG)

    logger.debug(f"Starting provider update for ID: {provider_id}")

    provider = db.session.query(IndividualProvider).get(provider_id)
    if provider is None:
        logger.error(f"Provider not found with ID: {provider_id}")
        return {"error": "Provider not found"}, 404

    # Fields to track for audit
    fields_to_track = {
        'npi': 'NPI',
        'first_name': 'First Name',
        'last_name': 'Last Name', 
        'gender': 'Gender',
        'phone': 'Phone',
        'provider_type': 'Provider Type',
        'accepting_new_patients': 'Accepting New Patients',
        'specialties': 'Specialties',
        'board_certifications': 'Board Certifications',
        'languages': 'Languages',
        'address_line': 'Address',
        'city': 'City',
        'state': 'State',
        'zip': 'ZIP',
        'provider_enrollment_form_image': 'Enrollment Form Image',
        'provider_enrollment_form_markdown_text': 'Enrollment Form Markdown',
        'provider_enrollment_form_json': 'Enrollment Form JSON',
        'provider_facets_tables': 'Provider Facets Tables',
        'provider_facets_markdown': 'Provider Facets Markdown'
    }

    try:
        audit_records = []
        field_updates = []

        logger.debug("Checking for field changes...")
        # First pass - collect all changes
        for field, display_name in fields_to_track.items():
            # Skip image field since it's handled separately
            if field == 'provider_enrollment_form_image':
                continue
                
            old_value = str(getattr(provider, field))
            new_value = str(request.form.get(field))

            # For boolean fields
            if field == 'accepting_new_patients':
                new_value = str(request.form.get(field) == 'true')

            if old_value != new_value:
                logger.debug(f"Change detected in {field}: {old_value} -> {new_value}")
                # Store the change
                field_updates.append((field, request.form.get(field), field == 'accepting_new_patients'))

                # Create audit record
                try:
                    logger.debug(f"Creating audit record for {field}")
                    logger.debug(f"Current user ID: {current_user.id if current_user.is_authenticated else 'None'}")

                    audit = ProviderAudit(
                        provider_id=provider_id,
                        field_updated=display_name,
                        old_value=old_value,
                        new_value=new_value,
                        change_description=f"Updated {display_name}",
                        user_id=current_user.id if current_user.is_authenticated else None
                    )
                    audit_records.append(audit)
                except Exception as e:
                    logger.error(f"Error creating audit record: {str(e)}")
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    raise

        # Second pass - apply all changes if audit records were created successfully
        logger.debug(f"Attempting to add {len(audit_records)} audit records")
        for audit in audit_records:
            try:
                db.session.add(audit)
                db.session.flush()  # Test if audit record can be created
                logger.debug(f"Successfully added audit record for {audit.field_updated}")
            except Exception as e:
                logger.error(f"Failed to create audit record: {str(e)}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                db.session.rollback()
                flash(f'Error creating audit record: {str(e)}')
                return redirect(url_for('providers.provider_detail', provider_id=provider_id))

        # Apply the actual field updates
        logger.debug("Applying field updates")
        for field, value, is_boolean in field_updates:
            logger.debug(f"Updating {field} to {value}")
            if field == 'provider_enrollment_form_image':
                # Skip image field in form update since it's handled separately
                continue
            elif field in ['provider_enrollment_form_json', 'provider_facets_tables']:
                # Store JSON as is
                setattr(provider, field, value if value else None)
            elif is_boolean:
                setattr(provider, field, value == 'true')
            else:
                setattr(provider, field, value)

        db.session.commit()
        logger.info("Provider update completed successfully")
        flash('Provider updated successfully')

    except Exception as e:
        logger.error(f"Failed to update provider: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        db.session.rollback()
        flash(f'Error updating provider: {str(e)}')

    return redirect(url_for('providers.provider_detail', provider_id=provider_id))