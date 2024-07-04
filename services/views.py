from django.shortcuts import render, get_object_or_404
from django.forms import inlineformset_factory
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify

from services.models import Client, Message, Mailing, Contact, Logs
from services.forms import ClientForm, MessageForm, MailingForm
# from services.mailing_task import send_email
# from services.services import homepage_cache
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
# from services.services import get_categories_from_cache, get_products_from_cache
from blog.models import Blog



class Homepage(TemplateView):
    """ Открывает главную форму проекта
    """
    Model = Logs
    template_name = "services/base.html"
    # random_article = Blog.objects.order_by('?')[:3]
    # random_article = Logs.objects.all()
    extra_context = {"title": "Сервис клиентских рассылок"}

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
        context_data["emails_unique_count"] = Client.objects.all().count()
        # context_data['random_blogs'] = get_articles_from_cache().order_by('created_at')[:3]
        context_data['random_blogs'] = Blog.objects.all().order_by('created_at')[:3]
        
        return context_data


class LogsListView(ListView):
    """ Выводит форму со статистикой рассылок"""
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
    """ Контроллер вывода списка клиентов
    """
    model = Client
    success_url = reverse_lazy("services:client_list")
    extra_context = {"title": "Список клиентов сервиса"}
    login_url = 'users:login'


    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        clients = Client.objects.all()
        context_data["clients_list"] = clients.filter(owner=self.request.user, is_active=True)
        return context_data


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    # Если используется форма ввода, то перечень полей не нужен
    # fields = ('name', 'email', 'comment',)
    success_url = reverse_lazy("services:client_list")
    extra_context = {"title": "Новый клиент"}
    login_url = 'users:login'
    redirect_field_name = "login"


    def form_valid(self, form):
      # Вызываем для заполнения поля 'owner'
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs



class ClientUpdateView(LoginRequiredMixin, UpdateView):
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


    def get_form_class(self):
        """ Открываем форму, зависящую от прав доступа
            и принадлежности пользователя к группе Manager"""
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            # для владельца товара
            return ClientForm
        elif (user.has_perm('services.can_reset_status')):
            # для Модератора
            # return ClientModeratorForm
            return ClientForm
        else:
            return ClientForm

        raise PermissionDenied



    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs

class ClientDetailView(DetailView):
    model = Client
    extra_context = {"title": "Информация о клиенте"}

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class ClientDeleteView(DeleteView):
    model = Client
    extra_context = {"title": "Удаление информации о клиенте"}
    success_url = reverse_lazy("services:client_list")


    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #     if self.request.user == self.object.owner or self.request.user.is_superuser:
    #         return self.object
    #     raise PermissionDenied

class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    success_url = reverse_lazy("services:message_list")
    extra_context = {"title": "СООБЩЕНИЯ"}
    login_url = 'users:login'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        # mess = Message.objects.all()
        # context_data["messages_list"] = mess.filter(owner=self.request.user)
        return context_data



class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("services:message_list")
    extra_context = {"title": "Создание сообщения"}
    login_url = 'users:login'

    # def form_valid(self, form):
    #     # Вызываем для заполнения поля Владелец сообщения
    #     self.object = form.save()
    #     self.object.owner = self.request.user
    #     self.object.save()
    #
    #     return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("services:message_list")
    extra_context = {"title": "Редактирование сообщения"}
    login_url = 'users:login'

    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #     if self.object.owner != self.request.user:
    #         raise Http404
    #     return self.object


class MessageDetailView(DetailView):
    model = Message
    extra_context = {"title": "Сообщение"}


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    extra_context = {"title": "Удаление сообщения"}
    success_url = reverse_lazy("services:message_list")
    login_url = 'users:login'


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    success_url = reverse_lazy("services:mailing_list")
    extra_context = {"title": "РАССЫЛКИ"}
    login_url = 'users:login'
    # permission_required = 'services.view_mailing'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        # context_data["mailing_list"] = Mailing.objects.all()
        context_data["mailing_list"] = Mailing.objects.filter(owner=self.request.user, is_active=True)
        unique_clients = Client.objects.filter(owner=self.request.user, is_active=True).count()
        context_data["clients"] = unique_clients
        context_data["mailing_count"] = Mailing.objects.filter(owner=self.request.user, is_active=True).count()
        return context_data

    # def get_queryset(self):
    #     """ Реализуем для пользователя request.user отбор только собственных активных рассылок"""
    #     queryset = super().get_queryset()
    #     # queryset = queryset.filter(id=self.kwargs.get('pk'))
    #     if not self.request.user.is_staff:
    #         queryset = queryset.filter(owner=self.request.user, is_active=True)
    #     else:
    #         queryset = queryset.filter(is_active=True)
    #
    #     return queryset
    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser and not user.has_perm("view_all_mailings"):
            raise PermissionDenied
        else:
            return queryset



class MailingCreateView(LoginRequiredMixin,CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("services:mailing_list")
    extra_context = {"title": "Создание рассылки"}
    login_url = 'users:login'

    def form_valid(self, form):
        # Вызываем для заполнения поля Владелец рассылки
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("services:mailing_list")
    extra_context = {"title": "Редактирование сообщения"}
    login_url = 'users:login'




# class MailingCreateView(CreateView):
#     model = Mailing
#     success_url = reverse_lazy("services:mailing_list")
#     extra_context = {"title": "Создание рассылки"}
#     fields = (
#         "name",
#         "status",
#         "periodicity",
#         "start_time",
#         "end_time",
#         "message",
#         "description",
#         "clients"
#     )

# class MailingUpdateView(UpdateView):
#     model = Mailing
#     fields = (
#         "name",
#         "status",
#         "periodicity",
#         "start_time",
#         "end_time",
#         "client",
#         "message",
#         "description",
#     )
#     success_url = reverse_lazy("services:mailing_list")
#     extra_context = {"title": "Редактирование рассылки"}
#     login_url = 'users:login'

    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #     if self.object.owner == self.request.user or self.request.user.is_superuser:
    #         return self.object
    #     else:
    #         raise Http404


class MailingDetailView(DetailView):
    model = Mailing
    extra_context = {"title": "Рассылка"}

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(id=self.kwargs.get('pk'))
    #     # if not self.request.user.is_staff:
    #     #     queryset = queryset.filter(owner=self.request.user)
    #     return queryset


class MailingDeleteView(DeleteView):
    model = Mailing
    extra_context = {"title": "Удаление рассылки"}
    success_url = reverse_lazy("services:mailing_list")
    # login_url = 'users:login'


class ContactsPageViews(CreateView):
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

