from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


from main.mixins import OwnerRequiredMixin
from recipients.forms import RecipientForm
from recipients.models import Recipient


class RecipientListView(PermissionRequiredMixin, ListView):
    model = Recipient
    permission_required = 'recipients.view_recipient'
    template_name = 'recipients/recipient_list.html'

    def get_queryset(self):
        if self.request.user.has_perm('recipients.view_recipient'):
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=self.request.user)


class RecipientDetailView(OwnerRequiredMixin, DetailView):
    model = Recipient


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy('recipients:recipient_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(OwnerRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy('recipients:recipient_list')


class RecipientDeleteView(OwnerRequiredMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy('recipients:recipient_list')
