
from typing import Dict, List
from models.db import db
from models.provider import IndividualProvider
from sqlalchemy import func

def check_provider_duplicates(provider_id: int) -> Dict:
    """
    Check for duplicate providers based on various matching criteria
    Returns JSON with duplicate status and detailed match information
    """
    provider = db.session.query(IndividualProvider).get(provider_id)

    if not provider:
        return {
            "overall_status": "No Provider Found",
            "duplicates": []
        }

    # Get all potential duplicates (excluding self)
    potential_duplicates = db.session.query(IndividualProvider)\
        .filter(IndividualProvider.provider_id != provider_id)\
        .filter(
            db.or_(
                IndividualProvider.npi == provider.npi,
                db.and_(
                    func.lower(IndividualProvider.first_name) == func.lower(provider.first_name),
                    func.lower(IndividualProvider.last_name) == func.lower(provider.last_name),
                    db.or_(
                        IndividualProvider.phone == provider.phone,
                        db.and_(
                            IndividualProvider.address_line == provider.address_line,
                            IndividualProvider.city == provider.city,
                            IndividualProvider.state == provider.state,
                            IndividualProvider.zip == provider.zip
                        )
                    )
                )
            )
        ).all()

    if not potential_duplicates:
        return {
            "overall_status": "No Potential Duplicates Found",
            "duplicates": []
        }

    duplicate_details = []
    for dup in potential_duplicates:
        # Compare each field to determine exact matches
        field_matches = {
            "npi": {
                "is_match": dup.npi == provider.npi,
                "duplicate_value": dup.npi,
                "original_value": provider.npi
            },
            "first_name": {
                "is_match": func.lower(dup.first_name) == func.lower(provider.first_name),
                "duplicate_value": dup.first_name,
                "original_value": provider.first_name
            },
            "last_name": {
                "is_match": func.lower(dup.last_name) == func.lower(provider.last_name),
                "duplicate_value": dup.last_name,
                "original_value": provider.last_name
            },
            "phone": {
                "is_match": dup.phone == provider.phone,
                "duplicate_value": dup.phone,
                "original_value": provider.phone
            },
            "address_line": {
                "is_match": dup.address_line == provider.address_line,
                "duplicate_value": dup.address_line,
                "original_value": provider.address_line
            },
            "city": {
                "is_match": dup.city == provider.city,
                "duplicate_value": dup.city,
                "original_value": provider.city
            },
            "state": {
                "is_match": dup.state == provider.state,
                "duplicate_value": dup.state,
                "original_value": provider.state
            },
            "zip": {
                "is_match": dup.zip == provider.zip,
                "duplicate_value": dup.zip,
                "original_value": provider.zip
            }
        }

        # Determine duplicate type
        is_exact_duplicate = dup.npi == provider.npi
        match_type = "Exact Match" if is_exact_duplicate else "Partial Match"

        duplicate_details.append({
            "duplicate_id": dup.provider_id,
            "match_type": match_type,
            "field_matches": field_matches,
            "duplicate_record": dup.to_dict()
        })

    return {
        "overall_status": "Potential Duplicates Found",
        "duplicates": duplicate_details
    }
