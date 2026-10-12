from django.contrib import admin

from recipients.models import Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "name", "description")
    search_fields = ("email", "name")
