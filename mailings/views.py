from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from mailings.forms import MailingForm
from mailings.models import Mailing
from mailings.services import send_mailing
from main.mixins import OwnerRequiredMixin


class MailingListView(PermissionRequiredMixin, ListView):
    model = Mailing
    permission_required = 'mailings.view_mailing'
    template_name = 'mailings/mailing_list.html'

    def get_queryset(self):
        if self.request.user.has_perm('mailings.view_mailing'):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(OwnerRequiredMixin, DetailView):
    model = Mailing


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(OwnerRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailing_list')


class MailingDeleteView(OwnerRequiredMixin, DeleteView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailing_list')


class MailingSendView(View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)

        try:
            result = send_mailing(mailing)
            messages.success(
                request,
                f"Рассылка запущена! Успешно: {result['success']}, Ошибок: {result['failed']}"
            )
        except ValueError as e:
            messages.error(request, str(e))

        return redirect('mailings:mailing_detail', pk=pk)


class MailingDisableView(PermissionRequiredMixin, View):
    permission_required = 'mailings.can_disable_mailing'

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)

        mailing.status = Mailing.STATUS_FINISHED
        mailing.save(update_fields=['status'])

        from django.contrib import messages
        messages.success(request, f'Рассылка #{mailing.pk} была принудительно отключена.')

        return redirect('mailings:mailing_list')
