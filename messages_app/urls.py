from django.urls import path
from messages_app.apps import MessagesAppConfig
from messages_app.views import MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, \
    MessageDeleteView

app_name = MessagesAppConfig.name

urlpatterns = [
    path('', MessageListView.as_view(), name='message_list'),
    path('<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('create/', MessageCreateView.as_view(), name='message_create'),
    path('update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
]