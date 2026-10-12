from django.urls import path
from recipients.apps import RecipientsConfig

from recipients.views import RecipientListView

app_name = RecipientsConfig.name


urlpatterns = [
    path('', RecipientListView.as_view(), name='recipient_list'),
]