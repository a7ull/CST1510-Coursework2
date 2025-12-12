from multi_domain_platform.models.security_incident import get_all_incidents, SecurityIncident

def get_all_incidents_page():
    return get_all_incidents()

def add_incident_page(incident_id, timestamp, severity, category, status, description):
    inc = SecurityIncident(incident_id, timestamp, severity, category, status, description)
    inc.save()

def delete_incident_page(incident_id):
    inc = SecurityIncident(incident_id, None, None, None, None, None)
    inc.incident_id = incident_id
    inc.delete()