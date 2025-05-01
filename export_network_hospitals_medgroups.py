
"""Export hospitals, networks, medical groups and their relationships to markdown tables.
This script queries the database and formats the data in markdown tables.
"""

from main import db, app
from models.hospital import Hospital
from models.network import Network
from models.medical_group import MedicalGroup
from models.REL_hospital_network import HospitalNetwork  
from models.REL_group_hospital import GroupHospital

def generate_markdown_tables():
    """Generate markdown tables for each entity and relationship."""
    
    # Query all data
    networks = db.session.query(Network).order_by(Network.network_id).all()
    hospitals = db.session.query(Hospital).order_by(Hospital.hospital_id).all()
    medical_groups = db.session.query(MedicalGroup).order_by(MedicalGroup.group_id).all()
    
    # Build the markdown string
    markdown = []
    
    # Networks table
    markdown.append("## networks\n")
    markdown.append("| ID | Code | Name |")
    markdown.append("|-----|------|------|")
    for network in networks:
        markdown.append(f"| {network.network_id} | {network.code} | {network.name} |")
    markdown.append("\n")
    
    # Hospitals table
    markdown.append("## hospitals\n") 
    markdown.append("| ID | Name |")
    markdown.append("|-----|------|")
    for hospital in hospitals:
        markdown.append(f"| {hospital.hospital_id} | {hospital.name} |")
    markdown.append("\n")
    
    # Medical Groups table
    markdown.append("## medical_groups\n")
    markdown.append("| ID | Name | Address |")
    markdown.append("|-----|------|---------|")
    for group in medical_groups:
        markdown.append(f"| {group.group_id} | {group.name} | {group.address_line or ''} |")
    markdown.append("\n")
    
    # Hospital-Network relationships
    markdown.append("## hospital_network\n")
    markdown.append("| Hospital ID | Network ID |")
    markdown.append("|------------|------------|")
    hospital_networks = db.session.query(HospitalNetwork).all()
    for rel in hospital_networks:
        markdown.append(f"| {rel.hospital_id} | {rel.network_id} |")
    markdown.append("\n")
    
    # Medical Group-Hospital relationships
    markdown.append("## group_hospital\n")
    markdown.append("| Medical Group ID | Hospital ID |")
    markdown.append("|-----------------|-------------|")
    group_hospitals = db.session.query(GroupHospital).all()
    for rel in group_hospitals:
        markdown.append(f"| {rel.group_id} | {rel.hospital_id} |")
    
    return "\n".join(markdown)

if __name__ == "__main__":
    with app.app_context():
        try:
            markdown_output = generate_markdown_tables()
            print(markdown_output)
        except Exception as e:
            print(f"Error generating markdown tables: {e}")
