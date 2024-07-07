from django import forms
from blog.models import Blog
from services.forms import StyleFormMixin


class BlogForm(StyleFormMixin, forms.ModelForm):
    """ Основная форма"""
    class Meta:
        model = Blog
        exclude = ("owner",)


class BlogManagerForm(StyleFormMixin, forms.ModelForm):
    """ Форма с ограниченным набором полей для пользователя с правами 'Manager' """
    class Meta:
        model = Blog
        fields = ("title", "is_published")
