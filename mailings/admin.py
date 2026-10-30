from django.contrib import admin
from .models import Mailing, MailingAttempt


class MailingAttemptInline(admin.TabularInline):
    model = MailingAttempt
    extra = 0
    readonly_fields = ('attempt_time', 'status', 'server_response', 'recipient')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'start_time')
    search_fields = ('message__subject',)
    ordering = ('-start_time',)

    inlines = [MailingAttemptInline]


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing', 'recipient', 'attempt_time', 'status')
    list_filter = ('status', 'attempt_time', 'mailing')
    search_fields = ('recipient__email', 'mailing__message__subject')
    ordering = ('-attempt_time',)

    readonly_fields = ('mailing', 'recipient', 'attempt_time', 'status', 'server_response')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
