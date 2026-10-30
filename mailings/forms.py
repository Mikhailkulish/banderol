from django import forms

from mailings.models import Mailing


class MailingForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        label='Дата и время начала отправки',
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M',  # ← формат для отображения
        ),
        input_formats=['%Y-%m-%dT%H:%M'],  # ← формат для ввода
    )
    end_time = forms.DateTimeField(
        label='Дата и время окончания отправки',
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M',
        ),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model = Mailing
        fields = ['start_time', 'end_time', 'message', 'recipients',]

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Укажите дату и время начала отправки'
        })

        self.fields['end_time'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Укажите дату и время окончания отправки'
        })

        self.fields['message'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Выберите сообщение'
        })

        self.fields['recipients'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Выберите получателей'
        })
