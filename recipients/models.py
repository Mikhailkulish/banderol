from django.db import models


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

    def __str__(self):
        return self.email

