from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from recipients.models import Recipient


class RecipientListView(ListView):
    model = Recipient
    template_name = 'recipients/recipient_list.html'

