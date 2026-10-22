from django.views.generic import TemplateView
from django.utils import timezone
from mailings.models import Mailing
from recipients.models import Recipient


class MainView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_mailings'] = Mailing.objects.count()

        now = timezone.now()
        context['active_mailings'] = Mailing.objects.filter(
            start_time__lte=now,
            end_time__gte=now,
            status=Mailing.STATUS_STARTED
        ).count()

        context['total_recipients'] = Recipient.objects.count()

        return context
