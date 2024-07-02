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

    def __init__(self, user, *args, **kwargs):
        """ Фильтруем рассылки
            Аргумент user передан в форму с помощью метода get_form_kwargs (см. ClientCreateView)
        """
        super().__init__(*args, **kwargs)
        self.fields['mailing'].queryset = Mailing.objects.filter(owner=user)

    class Meta:
        model = Client
        exclude = ("owner", "is_active",)




class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        exclude = ("owner", )



class MailingForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        exclude = ("clients","owner","is_active",)


