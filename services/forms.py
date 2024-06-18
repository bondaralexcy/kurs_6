from django import forms
from services.models import Client,Message,Mailing,Logs

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'email', 'comment',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('subject', 'body',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('name','status','periodicity','start_time', 'end_time','client','message','description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'