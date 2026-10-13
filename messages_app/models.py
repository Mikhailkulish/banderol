from django.db import models


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

    def __str__(self):
        return self.subject
