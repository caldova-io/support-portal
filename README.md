# Robobites Support Portal

A Django console for Robobites support teams handling delivery issues, robot status questions, refund requests, and customer follow-up.

## Features

- Ticket inbox grouped by customer and priority
- Ticket detail pages with reply notes and status changes
- Attachment intake for receipts, photos, and delivery logs
- Import endpoint for operations handoff bundles
- Priority labels driven by delivery context and issue age

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/` and set a `customer_key` cookie to view a customer queue.

## Daily usage

1. Start on the ticket inbox.
2. Search by reference, address, robot id, or customer name.
3. Open a ticket, add an agent response, and update the status.
4. Upload supporting material when a customer sends delivery photos or receipts.
5. Use imports for batched handoffs from operations.
