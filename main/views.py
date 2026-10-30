from django.views.generic import TemplateView
from django.utils import timezone
from django.core.cache import cache
from mailings.models import Mailing, MailingAttempt
from recipients.models import Recipient


class MainView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        if user.is_authenticated:
            # Формируем уникальный ключ для кеша конкретного пользователя
            cache_key = f"dashboard_stats_{user.id}"

            # Пытаемся достать статистику из Redis
            stats = cache.get(cache_key)

            # Если в кеше пусто, значит нужно посчитать и сохранить
            if stats is None:
                user_mailings = Mailing.objects.filter(owner=user)
                now = timezone.now()
                user_attempts = MailingAttempt.objects.filter(mailing__owner=user)

                stats = {
                    'total_mailings': user_mailings.count(),
                    'active_mailings': user_mailings.filter(
                        start_time__lte=now,
                        end_time__gte=now,
                        status=Mailing.STATUS_STARTED
                    ).count(),
                    'total_recipients': Recipient.objects.filter(owner=user).count(),
                    'successful_attempts': user_attempts.filter(status='Успешно').count(),
                    'failed_attempts': user_attempts.filter(status='Не успешно').count(),
                    'total_sent_messages': user_attempts.count(),
                }

                # Сохраняем словарь в Redis на 120 секунд (2 минуты)
                cache.set(cache_key, stats, timeout=120)

            # Обновляем контекст данными (из кеша или свежепосчитанными)
            context.update(stats)

        else:
            # Если пользователь не авторизован, показываем нули (это не кешируем)
            context.update({
                'total_mailings': 0,
                'active_mailings': 0,
                'total_recipients': 0,
                'successful_attempts': 0,
                'failed_attempts': 0,
                'total_sent_messages': 0,
            })

        return context
