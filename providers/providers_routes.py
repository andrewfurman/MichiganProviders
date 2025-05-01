from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, current_app
from main import db
from models import IndividualProvider, MedicalGroup, Hospital, Network, ProviderGroup, HospitalNetwork


providers_bp = Blueprint('providers', __name__, 
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/providers/static')

@providers_bp.route('/individual_providers/<int:provider_id>')
def provider_detail(provider_id):
    provider = db.session.query(IndividualProvider).get(provider_id)
    if provider is None:
        abort(404)

    medical_groups = db.session.query(MedicalGroup)\
        .join(ProviderGroup, ProviderGroup.group_id == MedicalGroup.group_id)\
        .filter(ProviderGroup.provider_id == provider_id)\
        .all()

    return render_template('individual_provider_detail.html', provider=provider, medical_groups=medical_groups)

@providers_bp.route('/individual_providers/<int:provider_id>/update', methods=['POST'])
def update_provider(provider_id):
    from providers.individual_provider_update import update_individual_provider
    return update_individual_provider(provider_id)

@providers_bp.route('/medical_groups')
def medical_groups():
    groups = db.session.query(MedicalGroup).order_by(MedicalGroup.group_id).all()
    return render_template('medical_groups.html', medical_groups=groups)

@providers_bp.route('/individual_providers')
def providers():
    providers = db.session.query(IndividualProvider).all()
    return render_template('individual_providers.html', providers=providers)

@providers_bp.route('/individual_providers/<int:provider_id>/delete', methods=['POST'])
def delete_provider(provider_id):
    provider = db.session.query(IndividualProvider).get(provider_id)
    if provider is None:
        abort(404)

    # First delete all provider group relationships
    db.session.query(ProviderGroup).filter(ProviderGroup.provider_id == provider_id).delete()
    
    # Then delete the provider
    db.session.delete(provider)
    db.session.commit()
    flash('Provider deleted successfully', 'success')
    return redirect(url_for('providers.providers'))

@providers_bp.route('/networks')
def networks():
    networks = db.session.query(Network).order_by(Network.network_id).all()
    return render_template('networks.html', networks=networks)

@providers_bp.route('/hospitals')
def hospitals():
    hospitals = db.session.query(Hospital).order_by(Hospital.hospital_id).all()
    return render_template('hospitals.html', hospitals=hospitals)

@providers_bp.route('/hospitals/<int:hospital_id>')
def hospital_detail(hospital_id):
    hospital = db.session.query(Hospital).get(hospital_id)
    if hospital is None:
        abort(404)
    
    networks = db.session.query(Network, HospitalNetwork)\
        .join(HospitalNetwork, Network.network_id == HospitalNetwork.network_id)\
        .filter(HospitalNetwork.hospital_id == hospital_id)\
        .all()
        
    return render_template('hospital_detail.html', hospital=hospital, networks=networks)

@providers_bp.route('/hospitals/<int:hospital_id>/update', methods=['POST'])
def update_hospital(hospital_id):
    hospital = db.session.query(Hospital).get(hospital_id)
    if hospital is None:
        abort(404)
        
    hospital.name = request.form.get('name')
    hospital.ccn = request.form.get('ccn')
    hospital.address_line = request.form.get('address_line')
    hospital.city = request.form.get('city')
    hospital.state = request.form.get('state')
    hospital.zip = request.form.get('zip')
    
    db.session.commit()
    flash('Hospital updated successfully', 'success')
    return redirect(url_for('providers.hospital_detail', hospital_id=hospital_id))