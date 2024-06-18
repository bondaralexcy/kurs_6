from django.shortcuts import render

# from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView,UpdateView,ListView,DetailView,DeleteView,TemplateView

# from blog.models import Blog
from services.models import Client, Message, Mailing, Contact, Logs
from services.forms import ClientForm, MessageForm, MailingForm
# from services.services import homepage_cache


class Homepage(TemplateView):
    template_name = 'services/base.html'
    # random_article = Blog.objects.order_by('?')[:3]
    # extra_context = {'title':'SkyService','filtred_list': homepage_cache()}
    extra_context = {'title': 'MessageMailing Service'}

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('services:client_list')
    # login_url = 'users:login'

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)

class ClientUpdateView(UpdateView):
    model = Client
    fields = ('name', 'email', 'comment',)
    success_url = reverse_lazy('services:client_list')
    # login_url = 'users:login'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner == self.request.user or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404

class ClientListView(ListView):
    model = Client
    success_url = reverse_lazy('services:client_list')
    extra_context = {'title': 'Список клиентов сервиса'}
    # login_url = 'users:login'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(id=self.kwargs.get('pk'))
        # if not self.request.user.is_staff:
        #     queryset = queryset.filter(owner=self.request.user)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args,**kwargs)
        context_data ['clients_list'] = Client.objects.all()
        return context_data

class ClientDetailView(DetailView):
    model = Client
    # login_url = 'users:login'

class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('services:client_list')
    # login_url = 'users:login'

# class MessageCreateView(CreateView):
#     model = Message
#     form_class = MessageForm
#     success_url = reverse_lazy('services:list_message')
#     login_url = 'users:login'
#
#     def form_valid(self, form):
#         self.object = form.save()
#         self.object.owner = self.request.user
#         self.object.save()
#
#         return super().form_valid(form)
#
# class MessageUpdateView(UpdateView):
#     model = Message
#     fields = ('subject', 'body',)
#     success_url = reverse_lazy('services:list_message')
#     login_url = 'users:login'
#
#     def get_object(self, queryset=None):
#         self.object = super().get_object(queryset)
#         if self.object.owner != self.request.user:
#             raise Http404
#         return self.object

# class MessageListView(ListView):
#     model = Message
#     success_url = reverse_lazy('services:list_message')
#     login_url = 'users:login'
#
#     def get_context_data(self, *args, **kwargs):
#         context_data = super().get_context_data(*args, **kwargs)
#         context_data['message_list'] = Message.objects.all()
#         return context_data
#
# class MessageDetailView(DetailView):
#     model = Message
#
#
# class MessageDeleteView(DeleteView):
#     model = Message
#     success_url = reverse_lazy('services:list_message')
#     login_url = 'users:login'
#
#
# class NewsletterCreateView(CreateView):
#     model = Newsletter
#     form_class = NewsletterForm
#     success_url = reverse_lazy('services:list_newsletter')
#     login_url = 'users:login'
#
#     def form_valid(self, form):
#         self.object = form.save()
#         self.object.owner = self.request.user
#         self.object.save()
#
#         return super().form_valid(form)
#
# class NewsletterUpdateView(UpdateView):
#     model = Newsletter
#     fields = ('start_time', 'end_time', 'periodicity', 'status', 'client', 'message')
#     success_url = reverse_lazy('services:list_newsletter')
#     login_url = 'users:login'
#
#     def get_object(self, queryset=None):
#         self.object = super().get_object(queryset)
#         if self.object.owner == self.request.user or self.request.user.is_superuser:
#             return self.object
#         else:
#             raise Http404
#
#
# class NewsletterListView(ListView):
#     model = Newsletter
#     success_url = reverse_lazy('services:list_newsletter')
#     login_url = 'users:login'
#     # permission_required = 'services.view_newsletter'
#
#     def get_context_data(self, *args, **kwargs):
#         context_data = super().get_context_data(*args, **kwargs)
#         context_data['newsletter_list'] = Newsletter.objects.all()
#         unique_clients = Client.objects.all().count()
#         context_data['clients'] = unique_clients
#         return context_data
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         queryset = queryset.filter(id=self.kwargs.get('pk'))
#         if not self.request.user.is_staff:
#             queryset = queryset.filter(owner = self.request.user)
#         return queryset
# class NewsletterDetailView(DetailView):
#     model = Newsletter
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         queryset = queryset.filter(id=self.kwargs.get('pk'))
#         if not self.request.user.is_staff:
#             queryset = queryset.filter(owner=self.request.user)
#         return queryset
#
# class NewsletterDeleteView(DeleteView):
#     model = Newsletter
#     success_url = reverse_lazy('services:list_newsletter')
#     login_url = 'users:login'
#
#
# class ContactTemplateView(TemplateView):
#     template_name = 'services/contacts.html'
#
#     def get_context_data(self, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#         contact_info = Contact.objects.all()
#         context_data['contact_book'] = contact_info
#         return context_data
#
#     def post(self,request):
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#         print(f'Имя:{name} , номер телефона:{phone} , сообщение: {message}')
#         return render(request,self.template_name)
#
#
# class LogsListView(ListView):
#     model = Logs
#     success_url = reverse_lazy('services:logs_list')
#     login_url = 'users:login'
#
#     def get_context_data(self, *args, **kwargs):
#         context_data = super().get_context_data(*args, **kwargs)
#         context_data['total'] = Logs.objects.all()
#         context_data['total_count'] = Logs.objects.all().count()
#         context_data['successful_count'] = Logs.objects.filter(attempt=True).count()
#         context_data['unsuccessful_count'] = Logs.objects.filter(attempt=False).count()
#         return context_data
#
