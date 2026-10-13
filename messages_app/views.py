from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from messages_app.forms import MessageForm
from messages_app.models import Message


class MessageListView(ListView):
    model = Message
    template_name = 'messages_app/message_list.html'


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('messages_app:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('messages_app:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('messages_app:message_list')
