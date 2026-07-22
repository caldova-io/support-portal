from dataclasses import dataclass
from datetime import timedelta
from django.utils import timezone


@dataclass(frozen=True)
class StatusStep:
    name: str
    label: str
    next_steps: tuple[str, ...]


STEPS = {
    "open": StatusStep("open", "Open", ("waiting", "resolved")),
    "waiting": StatusStep("waiting", "Waiting", ("open", "resolved")),
    "resolved": StatusStep("resolved", "Resolved", ()),
}


def allowed_statuses(current):
    step = STEPS.get(current, STEPS["open"])
    return [STEPS[name] for name in step.next_steps]


def priority_for(subject, description):
    text = f"{subject} {description}".lower()
    if any(word in text for word in ("stuck", "missing", "blocked", "refund")):
        return "high"
    if any(word in text for word in ("late", "cold", "spill")):
        return "urgent"
    return "normal"


def response_due_at(ticket):
    hours = {"urgent": 1, "high": 4, "normal": 12, "low": 24}.get(ticket.priority, 12)
    return ticket.created_at + timedelta(hours=hours)


def is_overdue(ticket):
    return ticket.status != "resolved" and response_due_at(ticket) < timezone.now()
