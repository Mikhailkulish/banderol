from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from messages_app.forms import MessageForm
from messages_app.models import Message


class MessageListView(ListView):
    model = Message
    template_name = 'messages_app/message_list.html'


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('messages_app:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('messages_app:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('messages_app:message_list')
