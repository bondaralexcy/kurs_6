from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.urls import reverse_lazy
from services.models import Client, Message, Mailing, Contact, Logs
from services.forms import ClientForm, MessageForm, MailingForm, MailingManagerForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from blog.models import Blog


class Homepage(TemplateView):
    """Открывает главную форму проекта"""

    Model = Logs
    template_name = "services/base.html"
    extra_context = {"title": "Сервис клиентских рассылок"}

    def get_context_data(self, *args, **kwargs):
        """Добавляем в контент информацию о рассылках и блогах"""
        context_data = super().get_context_data(*args, **kwargs)
        context_data["total"] = Logs.objects.all()
        context_data["total_count"] = Logs.objects.all().count()
        context_data["successful_count"] = Logs.objects.filter(
            attempt_status=True
        ).count()
        context_data["unsuccessful_count"] = Logs.objects.filter(
            attempt_status=False
        ).count()
        context_data["emails_unique_count"] = Client.objects.all().count()

        context_data["random_blogs"] = Blog.objects.all().order_by("created_at")[:3]

        return context_data


class LogsListView(ListView):
    """Выводит форму со статистикой рассылок"""

    model = Logs
    success_url = reverse_lazy("services:logs_list")
    extra_context = {"title": "Статистика рассылок"}

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data["total"] = Logs.objects.all()
        context_data["total_count"] = Logs.objects.all().count()
        context_data["successful_count"] = Logs.objects.filter(
            attempt_status=True
        ).count()
        context_data["unsuccessful_count"] = Logs.objects.filter(
            attempt_status=False
        ).count()
        return context_data


class ClientListView(LoginRequiredMixin, ListView):
    """Контроллер вывода списка клиентов"""

    model = Client
    success_url = reverse_lazy("services:client_list")
    extra_context = {"title": "Список клиентов сервиса"}
    login_url = "users:login"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        clients = Client.objects.all()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name="manager"):
            context_data["clients_list"] = clients.filter(owner=user, is_active=True)
        else:
            context_data["clients_list"] = clients

        return context_data


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Контроллер формы создания клиента"""

    model = Client
    form_class = ClientForm
    # Если используется форма ввода, то перечень полей не нужен
    # fields = ('name', 'email', 'comment',)
    success_url = reverse_lazy("services:client_list")
    extra_context = {"title": "Новый клиент"}
    login_url = "users:login"
    redirect_field_name = "login"

    def form_valid(self, form):
        # Вызываем для заполнения поля 'owner'
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        """Передаем current_user в форму"""
        kwargs = super().get_form_kwargs()
        kwargs["current_user"] = self.request.user
        return kwargs


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер обновления информации о клиенте"""

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("services:client_list")
    extra_context = {"title": "Обновление информации о клиенте"}

    def get_object(self, queryset=None):
        # Используется для проверки прав доступа к методу Update
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ClientDetailView(DetailView):
    """Выводит форму с детальной информацией о клиенте"""

    model = Client
    extra_context = {"title": "Информация о клиенте"}

    def get_object(self, queryset=None):
        # Используется для проверки прав доступа к методу DetailView
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class ClientDeleteView(DeleteView):
    """Контроллер удаления клиента
    Доступ контролируется в шаблоне меню
    """

    model = Client
    extra_context = {"title": "Удаление информации о клиенте"}
    success_url = reverse_lazy("services:client_list")


class MessageListView(LoginRequiredMixin, ListView):
    """Выводит форму со списком сообщений"""

    model = Message
    success_url = reverse_lazy("services:message_list")
    extra_context = {"title": "СООБЩЕНИЯ"}
    login_url = "users:login"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        return context_data


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания сообщения"""

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("services:message_list")
    extra_context = {"title": "Создание сообщения"}
    login_url = "users:login"


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер изменения сообщения"""

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("services:message_list")
    extra_context = {"title": "Редактирование сообщения"}
    login_url = "users:login"


class MessageDetailView(DetailView):
    """Контроллер отображения сообщения"""

    model = Message
    extra_context = {"title": "Сообщение"}


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер удаления сообщения"""

    model = Message
    extra_context = {"title": "Удаление сообщения"}
    success_url = reverse_lazy("services:message_list")
    login_url = "users:login"


class MailingListView(LoginRequiredMixin, ListView):
    """Контроллер вывода формы со списком рассылок"""

    model = Mailing
    success_url = reverse_lazy("services:mailing_list")
    extra_context = {"title": "РАССЫЛКИ"}
    login_url = "users:login"

    def get_context_data(self, *args, **kwargs):
        """Показываем пользователю только его рассылки
        Дополняем контент статистикой по рассылкам
        """
        context_data = super().get_context_data(*args, **kwargs)
        mailings = Mailing.objects.all()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name="manager"):
            context_data["mailing_list"] = mailings.filter(
                owner=self.request.user, is_active=True
            )
            unique_clients = Client.objects.filter(
                owner=self.request.user, is_active=True
            ).count()
            context_data["clients"] = unique_clients
            context_data["mailing_count"] = Mailing.objects.filter(
                owner=self.request.user, is_active=True
            ).count()
        else:
            # для Менеджера - полный список рассылок
            context_data["mailing_list"] = mailings

        return context_data

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser and not user.has_perm("can_view_all_mailings"):
            raise PermissionDenied
        else:
            return queryset


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Контроллер создания рассылки"""

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("services:mailing_list")
    extra_context = {"title": "Создание рассылки"}
    login_url = "users:login"

    def form_valid(self, form):
        # Вызываем для заполнения поля Владелец рассылки
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер изменения параметров рассылки"""

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("services:mailing_list")
    extra_context = {"title": "Редактирование рассылки"}
    login_url = "users:login"

    def get_object(self, queryset=None):
        # Используется для проверки прав доступа к методу Update
        self.object = super().get_object(queryset)
        user = self.request.user
        if (
            self.object.owner == user
            or user.is_superuser
            or user.groups.filter(name="manager")
        ):
            return self.object
        raise PermissionDenied

    def get_form_class(self):
        """Открываем форму, зависящую от прав доступа
        и принадлежности пользователя к группе Manager"""
        user = self.request.user
        if self.object.owner == user or user.is_superuser:
            # для владельца товара
            return MailingForm

        if user.has_perm("services.can_deactivate_mailing"):
            # для Менеджера
            return MailingManagerForm

        raise PermissionDenied


class MailingDetailView(DetailView):
    """Контроллер отображения рассылки"""

    model = Mailing
    extra_context = {"title": "Рассылка"}


class MailingDeleteView(DeleteView):
    """Контроллер удаления рассылки"""

    model = Mailing
    extra_context = {"title": "Удаление рассылки"}
    success_url = reverse_lazy("services:mailing_list")


class ContactsPageViews(CreateView):
    """Отображение списка из 5 контактов"""

    model = Contact
    fields = (
        "name",
        "phone",
        "email",
        "message",
    )
    success_url = reverse_lazy("services:contacts")
    template_name = "services/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        number = len(Contact.objects.all())
        if number > 5:
            context["latest_contacts"] = Contact.objects.all()[number - 5 : number + 1]
        else:
            context["latest_contacts"] = Contact.objects.all()
        return context


def contacts(request):
    """Метод ввода информации о контакте"""
    number = len(Contact.objects.all())
    if number > 5:
        contacts_list = Contact.objects.all()[number - 5 : number + 1]
    else:
        contacts_list = Contact.objects.all()

    context = {"object_list": contacts_list, "title": "Контакты"}

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        message = request.POST.get("message")

        info = {
            "time": (datetime.now()).strftime("%Y-%m-%dT%H:%M:%S.%f"),
            "name": name,
            "phone": phone,
            "email": email,
            "message": message,
        }

        Contact.objects.create(**info)

    return render(request, "services/contacts.html", context)
