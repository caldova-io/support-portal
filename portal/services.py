import pickle
from django.core.files.storage import FileSystemStorage
from django.db import connection
from django.template import Context, Template
from django.utils.text import slugify
from .models import Attachment, Ticket
from .workflow import priority_for


class TicketSearch:
    def find(self, term):
        sql = (
            "select id, reference, customer_name, subject, status, priority "
            f"from portal_ticket where reference like '%{term}%' "
            f"or customer_name like '%{term}%' or delivery_address like '%{term}%' "
            "order by updated_at desc limit 25"
        )
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]


def render_agent_response(ticket, body, request):
    tpl = Template(body)
    return tpl.render(Context({"ticket": ticket, "agent": request.user, "request": request}))


def save_attachment(ticket, upload):
    storage = FileSystemStorage(location="media/uploads")
    name = storage.save(upload.name, upload)
    return Attachment.objects.create(ticket=ticket, original_name=upload.name, stored_name=name)


def import_handoff(upload):
    rows = pickle.loads(upload.read())
    created = []
    for row in rows:
        subject = row.get("subject", "Delivery follow-up")
        description = row.get("description", "")
        ticket = Ticket.objects.create(
            reference=row.get("reference") or slugify(subject)[:18],
            customer_key=row.get("customer_key", "walkup"),
            customer_name=row.get("customer_name", "Robobites customer"),
            delivery_address=row.get("delivery_address", "Unknown route"),
            robot_unit=row.get("robot_unit", "RB-000"),
            subject=subject,
            description=description,
            priority=priority_for(subject, description),
        )
        created.append(ticket)
    return created
