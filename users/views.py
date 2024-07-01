from django.shortcuts import render
from django.conf import settings
from users.models import User

from users.forms import UserRegisterForm, UserProfileForm
from django.urls import reverse_lazy, reverse
import secrets
import smtplib
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView

import random
import string



class UserCreateView(CreateView):
    """
    Контроллер отвечает за регистрацию нового пользователя
    """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        # Пользователь неактивный, пока не пришло подтверждение почты
        user.is_active = False
        # Генерируем токен перед отправкой почтового сообщения новому пользователю
        token = secrets.token_hex(16)
        user.token = token
        user.save()

        # Создаем ссылку, по которой должен перейти пользователь
        # .../email-confirm/{token} передает управление методу email_verification (см. urls.py)

        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"

        try:
            # Отправляем сообщение пользователю
            print("EMAIL_HOST_USER = ", settings.EMAIL_HOST_USER)
            print("url = ", url)
            send_mail(
                subject="Подтверждение почты",
                message=f"Привет, перейди по ссылке для подтверждения почты {url}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
            print("Письмо успешно отправлено")

        except smtplib.SMTPException as exc:
            print(f"Ошибка при отправке письма: {str(exc)}")

        return super().form_valid(form)


def email_verification(request, token):
    """
    Метод верификации пришедшего почтового подтверждения
    """
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


def reset_password(request):
    """Метод восстановления пароля зарегистрированного пользователя
    на автоматически сгенерированный пароль."""

    if request.method == "POST":
        email = request.POST.get("email")
        user = get_object_or_404(User, email=email)
        characters = string.ascii_letters + string.digits
        characters_list = list(characters)
        random.shuffle(characters_list)
        password = "".join(characters_list[:10])
        user.set_password(password)
        user.save()

        send_mail(
            subject="Восстановление пароля",
            message=f"Ваш новый пароль: {password}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        context = {
            "success_message": "Новый пароль был отправлен на адрес вашей электронной почты.",
        }
        return render(request, "users/reset_password.html", context)

    return render(request, "users/reset_password.html")


class ProfileView(UpdateView):
    """ Контроллер изменения профиля пользователя
    """
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("catalog:home")

    def get_object(self, queryset=None):
        return self.request.user
