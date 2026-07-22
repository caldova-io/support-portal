from django.contrib import admin
from .models import Attachment, Ticket, TicketNote


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("reference", "customer_name", "status", "priority", "robot_unit", "created_at")
    search_fields = ("reference", "customer_name", "delivery_address", "robot_unit")


admin.site.register(TicketNote)
admin.site.register(Attachment)
