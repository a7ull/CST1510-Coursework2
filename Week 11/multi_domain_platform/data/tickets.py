from multi_domain_platform.models.it_ticket import get_all_tickets, ITTicket

def get_all_tickets_page():
    return get_all_tickets()

def add_ticket_page(ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours):
    t = ITTicket(ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours)
    t.save()

def delete_ticket_page(ticket_id):
    t = ITTicket(ticket_id, None, None, None, None, None, None)
    t.ticket_id = ticket_id
    t.delete()