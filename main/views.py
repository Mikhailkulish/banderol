from django.views.generic import TemplateView
from django.utils import timezone
from mailings.models import Mailing, MailingAttempt
from recipients.models import Recipient
from django.db.models import Count


class MainView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        if user.is_authenticated:
            # 1. Общее количество рассылок пользователя
            user_mailings = Mailing.objects.filter(owner=user)
            context['total_mailings'] = user_mailings.count()

            # 2. Активные рассылки (по времени)
            now = timezone.now()
            context['active_mailings'] = user_mailings.filter(
                start_time__lte=now,
                end_time__gte=now,
                status=Mailing.STATUS_STARTED
            ).count()

            # 3. Уникальные получатели пользователя
            context['total_recipients'] = Recipient.objects.filter(owner=user).count()

            # 4. Статистика попыток
            # Берем все попытки, которые относятся к рассылкам текущего пользователя
            user_attempts = MailingAttempt.objects.filter(mailing__owner=user)

            # Считаем успешные и неуспешные
            context['successful_attempts'] = user_attempts.filter(status='Успешно').count()
            context['failed_attempts'] = user_attempts.filter(status='Не успешно').count()

            # Считаем общее количество отправленных сообщений (все попытки)
            context['total_sent_messages'] = user_attempts.count()

        else:
            # Если пользователь не авторизован, показываем нули
            context.update({
                'total_mailings': 0,
                'active_mailings': 0,
                'total_recipients': 0,
                'successful_attempts': 0,
                'failed_attempts': 0,
                'total_sent_messages': 0,
            })

        return context
