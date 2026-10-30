from django.urls import path
from mailings.apps import MailingsConfig
from mailings.views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView, \
    MailingSendView, MailingDisableView

app_name = MailingsConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
    path('update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('<int:pk>/send/', MailingSendView.as_view(), name='mailing_send'),
    path('<int:pk>/disable/', MailingDisableView.as_view(), name='mailing_disable'),
]
