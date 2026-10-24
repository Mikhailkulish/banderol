from django.db import models
from django.conf import settings


class Message(models.Model):
    subject = models.CharField(
        max_length=255,
        verbose_name="Тема сообщения",
        help_text="Укажите тему сообщения"
    )
    body = models.TextField(
        verbose_name="Содержание сообщения",
        help_text="Введите сообщение"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Владелец',
        null=True, blank=True
    )

    def __str__(self):
        return self.subject
