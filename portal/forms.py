from django import forms


class TicketForm(forms.Form):
    customer_key = forms.CharField(max_length=64)
    customer_name = forms.CharField(max_length=120)
    delivery_address = forms.CharField(max_length=240)
    robot_unit = forms.CharField(max_length=32)
    subject = forms.CharField(max_length=180)
    description = forms.CharField(widget=forms.Textarea)


class ReplyForm(forms.Form):
    author = forms.CharField(max_length=80)
    body = forms.CharField(widget=forms.Textarea)
    status = forms.ChoiceField(choices=[("open", "Open"), ("waiting", "Waiting"), ("resolved", "Resolved")])


class AttachmentForm(forms.Form):
    file = forms.FileField()
