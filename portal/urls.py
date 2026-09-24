from django.urls import path
from . import exports, views

app_name = "portal"

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path("tickets/new/", views.new_ticket, name="new_ticket"),
    path("tickets/search/", views.search, name="search"),
    path("tickets/<int:ticket_id>/", views.ticket_detail, name="ticket_detail"),
    path("tickets/<int:ticket_id>/reply/", views.reply, name="reply"),
    path("tickets/<int:ticket_id>/attachments/", views.upload_attachment, name="upload_attachment"),
    path("tickets/export/", exports.export_ticket, name="export_ticket"),
    path("imports/", views.imports, name="imports"),
]
