from django.urls import path
from recipients.apps import RecipientsConfig

from recipients.views import RecipientListView, RecipientDetailView, RecipientCreateView

app_name = RecipientsConfig.name


urlpatterns = [
    path('', RecipientListView.as_view(), name='recipient_list'),
    path('recipient/<int:pk>', RecipientDetailView.as_view(), name='recipient_detail'),
    path('create/', RecipientCreateView.as_view(), name='recipient_create')
]