from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from recipients.forms import RecipientForm
from recipients.models import Recipient


class RecipientListView(ListView):
    model = Recipient
    template_name = 'recipients/recipient_list.html'


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy('recipients:recipient_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy('recipients:recipient_list')


class RecipientDeleteView(DeleteView):
    model = Recipient
    success_url = reverse_lazy('recipients:recipient_list')
