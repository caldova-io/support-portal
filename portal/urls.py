from django.urls import path
from . import views

app_name = "portal"

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path("tickets/new/", views.new_ticket, name="new_ticket"),
    path("tickets/search/", views.search, name="search"),
    path("tickets/<int:ticket_id>/", views.ticket_detail, name="ticket_detail"),
    path("tickets/<int:ticket_id>/reply/", views.reply, name="reply"),
    path("tickets/<int:ticket_id>/attachments/", views.upload_attachment, name="upload_attachment"),
    path("imports/", views.imports, name="imports"),
]
