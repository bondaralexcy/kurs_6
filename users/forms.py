from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from users.models import User



class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-control"


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Регистравция нового пользователя с помощью стандартной формы UserCreationForm"""
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class UserProfileForm(StyleFormMixin, UserChangeForm):
    """Изменение профиля пользователя с помощью стандартной формы UserChangeForm"""
    class Meta:
        model = User
        fields = ("email", "phone", "country", "avatar")

    def __init__(self, *args, **kwargs):
        """Подавление вывода предупреждения о пароле"""
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.HiddenInput()
