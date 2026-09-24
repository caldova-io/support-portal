from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Ticket


def export_ticket(request):
    ticket_id = request.GET.get("ticket_id")
    ticket = get_object_or_404(Ticket, id=ticket_id)

    return JsonResponse({
        "reference": ticket.reference,
        "customer_key": ticket.customer_key,
        "customer_name": ticket.customer_name,
        "delivery_address": ticket.delivery_address,
        "robot_unit": ticket.robot_unit,
        "subject": ticket.subject,
        "description": ticket.description,
        "status": ticket.status,
        "priority": ticket.priority,
    })
