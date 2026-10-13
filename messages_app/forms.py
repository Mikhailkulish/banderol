from django import forms
from django.core.exceptions import ValidationError

from messages_app.models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body',]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите тему собщения'
        })

        self.fields['body'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите содержание сообщения'
        })
