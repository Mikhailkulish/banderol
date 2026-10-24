from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings


class Mailing(models.Model):
    STATUS_CREATED = 'Создана'
    STATUS_STARTED = 'Запущена'
    STATUS_FINISHED = 'Завершена'

    STATUS_CHOICES = [
        (STATUS_CREATED, 'Создана'),
        (STATUS_STARTED, 'Запущена'),
        (STATUS_FINISHED, 'Завершена'),
    ]

    start_time = models.DateTimeField(
        verbose_name="Дата и время начала отправки",
        help_text="Укажите дату и время начала отправки"
    )
    end_time = models.DateTimeField(
        verbose_name="Дата и время окончания отправки",
        help_text="Укажите дату и время окончания отправки"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CREATED,
        verbose_name='Статус',
    )
    message = models.ForeignKey(
        'messages_app.Message',
        on_delete=models.CASCADE,
        related_name='mailings',
        verbose_name='Сообщение',
    )
    recipients = models.ManyToManyField(
        'recipients.Recipient',
        related_name='mailings',
        verbose_name='Получатели',
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mailings',
        verbose_name='Владелец',
        null=True, blank=True
    )

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f'Рассылка #{self.pk} — {self.message.subject}'

    def update_status(self):
        now = timezone.now()

        if now < self.start_time:
            new_status = self.STATUS_CREATED
        elif self.start_time <= now <= self.end_time:
            new_status = self.STATUS_STARTED
        else:
            new_status = self.STATUS_FINISHED

        if self.status != new_status:
            self.status = new_status
            self.save(update_fields=['status'])

    def clean(self):
        super().clean()

        if self.start_time and self.start_time < timezone.now():
            raise ValidationError({
                'start_time': 'Дата начала не может быть в прошлом.'
            })

        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError({
                'end_time': 'Дата окончания должна быть позже даты начала.'
            })


class MailingAttempt(models.Model):
    STATUS_SUCCESS = 'Успешно'
    STATUS_FAILED = 'Не успешно'

    STATUS_CHOICES = [
        (STATUS_SUCCESS, 'Успешно'),
        (STATUS_FAILED, 'Не успешно'),
    ]

    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name='Рассылка',
    )
    recipient = models.ForeignKey(
        'recipients.Recipient',
        on_delete=models.CASCADE,
        verbose_name='Получатель',
        null=True, blank=True, # На случай, если ошибка произошла до определения получателя
    )
    attempt_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время попытки',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name='Статус',
    )
    server_response = models.TextField(
        blank=True,
        verbose_name='Ответ сервера',
        help_text='Текст ошибки или ответ почтового сервера',
    )

    class Meta:
        verbose_name = 'Попытка отправки'
        verbose_name_plural = 'Попытки отправки'
        ordering = ['-attempt_time']

    def __str__(self):
        return f'Попытка {self.pk} для рассылки {self.mailing.pk} - {self.status}'
