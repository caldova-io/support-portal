from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import AttachmentForm, ReplyForm, TicketForm
from .models import Ticket, TicketNote
from .services import TicketSearch, import_handoff, render_agent_response, save_attachment
from .workflow import allowed_statuses, is_overdue, priority_for, response_due_at


def current_customer(request):
    return request.COOKIES.get("customer_key", "cst-north-loop")


def inbox(request):
    tickets = Ticket.objects.filter(customer_key=current_customer(request)).order_by("-updated_at")[:50]
    return render(request, "portal/inbox.html", {"tickets": tickets, "is_overdue": is_overdue})


def new_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ticket = Ticket.objects.create(
                reference=f"RB-{Ticket.objects.count() + 1001}",
                customer_key=data["customer_key"],
                customer_name=data["customer_name"],
                delivery_address=data["delivery_address"],
                robot_unit=data["robot_unit"],
                subject=data["subject"],
                description=data["description"],
                priority=priority_for(data["subject"], data["description"]),
            )
            return redirect("portal:ticket_detail", ticket_id=ticket.id)
    else:
        form = TicketForm(initial={"customer_key": current_customer(request)})
    return render(request, "portal/new_ticket.html", {"form": form})


def search(request):
    term = request.GET.get("q", "")
    results = TicketSearch().find(term) if term else []
    return render(request, "portal/search.html", {"term": term, "results": results})


def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, "portal/detail.html", {
        "ticket": ticket,
        "reply_form": ReplyForm(initial={"status": ticket.status}),
        "attachment_form": AttachmentForm(),
        "next_steps": allowed_statuses(ticket.status),
        "due_at": response_due_at(ticket),
    })


def reply(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    form = ReplyForm(request.POST)
    if request.method == "POST" and form.is_valid():
        body = render_agent_response(ticket, form.cleaned_data["body"], request)
        TicketNote.objects.create(ticket=ticket, author=form.cleaned_data["author"], body=body)
        ticket.status = form.cleaned_data["status"]
        ticket.save(update_fields=["status", "updated_at"])
        messages.success(request, "Response added.")
    return redirect("portal:ticket_detail", ticket_id=ticket.id)


def upload_attachment(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    form = AttachmentForm(request.POST, request.FILES)
    if request.method == "POST" and form.is_valid():
        save_attachment(ticket, form.cleaned_data["file"])
        messages.success(request, "Attachment stored.")
    return redirect("portal:ticket_detail", ticket_id=ticket.id)


def imports(request):
    created = []
    if request.method == "POST" and request.FILES.get("bundle"):
        created = import_handoff(request.FILES["bundle"])
        messages.success(request, f"Imported {len(created)} tickets.")
    return render(request, "portal/imports.html", {"created": created})
