from django.urls import path
from services.apps import ServicesConfig
from services.views import Homepage
from services.views import ContactsPageViews
from services.services import poster
from django.views.decorators.cache import cache_page

from services.views import (
    ClientCreateView,
    ClientListView,
    ClientDetailView,
    ClientUpdateView,
    ClientDeleteView,
)
from services.views import (
    MessageCreateView,
    MessageListView,
    MessageDetailView,
    MessageUpdateView,
    MessageDeleteView,
)
from services.views import (
    MailingCreateView,
    MailingUpdateView,
    MailingListView,
    MailingDetailView,
    MailingDeleteView,
)
from services.views import LogsListView

# from django.views.decorators.cache import cache_page

app_name = ServicesConfig.name

urlpatterns = [
    # Кешировать контроллер главной страницы
    #  --> cache_page(60)(Homepage.as_view()) вместо Homepage.as_view()
    # приводит к тому, что кешируется информация о текущем пользователе,
    # что не дает корректно обрабатывать ситуацию user.is_authenticated
    path("", Homepage.as_view(), name="home"),
    path("contacts/", ContactsPageViews.as_view(), name="contacts"),
    path("client_list/", ClientListView.as_view(), name="client_list"),
    path("create_client/", ClientCreateView.as_view(), name="create_client"),
    path("view_client/<int:pk>", ClientDetailView.as_view(), name="view_client"),
    path("edit_client/<int:pk>", ClientUpdateView.as_view(), name="edit_client"),
    path("delete_client/<int:pk>", ClientDeleteView.as_view(), name="delete_client"),
    path("message_list/", MessageListView.as_view(), name="message_list"),
    path("message/create", MessageCreateView.as_view(), name="create_message"),
    # Кешируем контроллер показа информации о сообщениях
    path(
        "message/view/<int:pk>",
        cache_page(60)(MessageDetailView.as_view()),
        name="view_message",
    ),
    path("message/edit/<int:pk>", MessageUpdateView.as_view(), name="edit_message"),
    path("message/delete/<int:pk>", MessageDeleteView.as_view(), name="delete_message"),
    path("mailing_list/", MailingListView.as_view(), name="mailing_list"),
    path("mailing/create", MailingCreateView.as_view(), name="create_mailing"),
    path("mailing/edit/<int:pk>", MailingUpdateView.as_view(), name="edit_mailing"),
    path("mailing/view/<int:pk>", MailingDetailView.as_view(), name="view_mailing"),
    path("mailing/delete/<int:pk>", MailingDeleteView.as_view(), name="delete_mailing"),
    path("logs/", LogsListView.as_view(), name="logs_list"),
    path("poster/", poster, name="poster"),
]
