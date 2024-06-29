from django import forms
from django.forms import ModelForm
from services.models import Client, Message, Mailing, Logs


class StyleFormMixin:
    """Класс-миксин для оформления в едином стиле"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-control"



class ClientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        fields = "__all__"


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = (
            "subject",
            "body",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class MailingForm(ModelForm):
    class Meta:
        model = Mailing
        fields = (
            "name",
            "status",
            "periodicity",
            "start_time",
            "end_time",
            "client",
            "message",
            "description",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
