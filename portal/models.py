from django.db import models
from django.utils import timezone


class Ticket(models.Model):
    STATUS_CHOICES = [("open", "Open"), ("waiting", "Waiting"), ("resolved", "Resolved")]
    PRIORITY_CHOICES = [("low", "Low"), ("normal", "Normal"), ("high", "High"), ("urgent", "Urgent")]

    reference = models.CharField(max_length=24, unique=True)
    customer_key = models.CharField(max_length=64, db_index=True)
    customer_name = models.CharField(max_length=120)
    delivery_address = models.CharField(max_length=240)
    robot_unit = models.CharField(max_length=32)
    subject = models.CharField(max_length=180)
    description = models.TextField()
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="open")
    priority = models.CharField(max_length=16, choices=PRIORITY_CHOICES, default="normal")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reference} {self.subject}"


class TicketNote(models.Model):
    ticket = models.ForeignKey(Ticket, related_name="notes", on_delete=models.CASCADE)
    author = models.CharField(max_length=80)
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["created_at"]


class Attachment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name="attachments", on_delete=models.CASCADE)
    original_name = models.CharField(max_length=180)
    stored_name = models.CharField(max_length=240)
    uploaded_at = models.DateTimeField(default=timezone.now)
