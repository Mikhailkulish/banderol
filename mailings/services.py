from django.core.mail import send_mail
from django.utils import timezone
from .models import MailingAttempt


def send_mailing(mailing):
    now = timezone.now()
    if not (mailing.start_time <= now <= mailing.end_time):
        raise ValueError("Отправка запрещена: текущее время вне интервала рассылки.")

    recipients = mailing.recipients.all()
    if not recipients.exists():
        raise ValueError("Нет получателей для отправки.")

    success_count = 0
    failed_count = 0

    for recipient in recipients:
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=None,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            MailingAttempt.objects.create(
                mailing=mailing, recipient=recipient, status=MailingAttempt.STATUS_SUCCESS
            )
            success_count += 1
        except Exception as e:
            MailingAttempt.objects.create(
                mailing=mailing, recipient=recipient, status=MailingAttempt.STATUS_FAILED, server_response=str(e)
            )
            failed_count += 1

    return {'success': success_count, 'failed': failed_count}
