from django.db import models

from django.conf import settings


class Recipient(models.Model):
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Введите Email",
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Получатель рассылки",
        help_text="Введите ФИО получателя рассылки",
    )
    description = models.TextField(blank=True,)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipients',
        verbose_name='Владелец',
        null=True, blank=True
    )

    def __str__(self):
        return self.email
