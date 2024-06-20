from django.shortcuts import render

# from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    ListView,
    DetailView,
    DeleteView,
    TemplateView,
)

# from blog.models import Blog
from services.models import Client, Message, Mailing, Contact, Logs
from services.forms import ClientForm, MessageForm, MailingForm

# from services.services import homepage_cache


class Homepage(TemplateView):
    Model = Logs
    template_name = "services/base.html"
    # random_article = Blog.objects.order_by('?')[:3]
    random_article = Logs.objects.all()
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
        return context_data


class LogsListView(ListView):
    model = Logs
    success_url = reverse_lazy("services:logs_list")
    extra_context = {"title": "Статистика рассылок"}
    # login_url = 'users:login'

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


class ClientListView(ListView):
    model = Client
    success_url = reverse_lazy("services:client_list")
    extra_context = {"title": "Список клиентов сервиса"}
    # login_url = 'users:login'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(id=self.kwargs.get("pk"))
        # if not self.request.user.is_staff:
        #     queryset = queryset.filter(owner=self.request.user)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data["clients_list"] = Client.objects.all()
        return context_data


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    # Если используется форма ввода, то перечень полей не нужен
    # fields = ('name', 'email', 'comment',)
    success_url = reverse_lazy("services:client_list")
    extra_context = {"title": "Новый клиент"}
    # login_url = 'users:login'

    # def form_valid(self, form):
    #   # Используется для заполнения поля  'owner'
    #     self.object = form.save()
    #     self.object.owner = self.request.user
    #     self.object.save()
    #
    #     return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    # fields = ('name', 'email', 'comment',)
    form_class = ClientForm
    success_url = reverse_lazy("services:client_list")
    extra_context = {"title": "Обновление информации о клиенте"}
    # login_url = 'users:login'

    # def get_object(self, queryset=None):
    ## Используется для проверки прав доступа к методу Update
    # self.object = super().get_object(queryset)
    # if self.object.owner == self.request.user or self.request.user.is_superuser:
    #     return self.object
    # else:
    #     raise Http404


class ClientDetailView(DetailView):
    model = Client
    extra_context = {"title": "Информация о клиенте"}
    # login_url = 'users:login'


class ClientDeleteView(DeleteView):
    model = Client
    extra_context = {"title": "Удаление информации о клиенте"}
    success_url = reverse_lazy("services:client_list")
    # login_url = 'users:login'


class MessageListView(ListView):
    model = Message
    success_url = reverse_lazy("services:message_list")
    extra_context = {"title": "СООБЩЕНИЯ"}
    # login_url = 'users:login'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data["message_list"] = Message.objects.all()
        return context_data


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("services:message_list")
    extra_context = {"title": "Создание сообщения"}
    # login_url = 'users:login'

    # def form_valid(self, form):
    #     self.object = form.save()
    #     self.object.owner = self.request.user
    #     self.object.save()
    #
    #     return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("services:message_list")
    extra_context = {"title": "Редактирование сообщения"}
    # login_url = 'users:login'

    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #     if self.object.owner != self.request.user:
    #         raise Http404
    #     return self.object


class MessageDetailView(DetailView):
    model = Message
    extra_context = {"title": "Сообщение"}


class MessageDeleteView(DeleteView):
    model = Message
    extra_context = {"title": "Удаление сообщения"}
    success_url = reverse_lazy("services:message_list")
    # login_url = 'users:login'


class MailingListView(ListView):
    model = Mailing
    success_url = reverse_lazy("services:mailing_list")
    extra_context = {"title": "РАССЫЛКИ"}
    # login_url = 'users:login'
    # permission_required = 'services.view_mailing'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data["mailing_list"] = Mailing.objects.all()
        unique_clients = Client.objects.all().count()
        context_data["clients"] = unique_clients
        context_data["mailing_count"] = Mailing.objects.all().count()
        return context_data

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(id=self.kwargs.get('pk'))
    #     # if not self.request.user.is_staff:
    #     #     queryset = queryset.filter(owner = self.request.user)
    #     return queryset


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("services:mailing_list")
    extra_context = {"title": "Создание рассылки"}
    # login_url = 'users:login'

    # def form_valid(self, form):
    #     self.object = form.save()
    #     self.object.owner = self.request.user
    #     self.object.save()

    # return super().form_valid(form)


class MailingUpdateView(UpdateView):
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
    success_url = reverse_lazy("services:mailing_list")
    extra_context = {"title": "Редактирование рассылки"}
    # login_url = 'users:login'

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


# class ContactTemplateView(TemplateView):
#     template_name = 'services/bad_contacts.html'
#     extra_context = {'title': 'Контакты'}
#
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["latest_contacts"] = Contact.objects.all()[:5]
#         # contact_info = Contact.objects.all()
#         # context['contact_book'] = contact_info
#         return context
#
#     def post(self, request):
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         email = request.POST.get('email')
#         print(f'Имя:{name} , номер телефона:{phone} , эл.почта: {email}')
#         return render(request, self.template_name)
