from django.contrib import admin
from messages_app.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject",)
    list_filter = ("subject",)
    search_fields = ("subject", "body")
    ordering = ("subject",)
