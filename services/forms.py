from django.forms import ModelForm
from services.models import Client, Message, Mailing, Logs


class ClientForm(ModelForm):
    class Meta:
        model = Client
        # Перечислить нужные поля
        # fields = (
        #     "name",
        #     "email",
        #     "comment",
        # )
        # В случае, если все поля
        fields = "__all__"
        # Можно задать исключение полей
        # exclude ("owner",)

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
