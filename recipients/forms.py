from django import forms
from django.core.exceptions import ValidationError

from recipients.models import Recipient


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['email', 'name', 'description',]

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not name:
            return name

        if not all(c.isalpha() or c.isspace() or c == '-' for c in name):
            raise ValidationError('Ф. И. О. может содержать только буквы, пробелы и дефис.')
        return name

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите адрес почты'
        })

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите фамилию, имя, отчество'
        })

        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите описание'
        })
