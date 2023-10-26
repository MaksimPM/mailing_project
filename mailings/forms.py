from django import forms

from mailings.models import Mailings, Message, Client


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailings
        exclude = ('user', 'is_active')
        help_texts = {
            'clients': 'Удерживайте “Control“ (или “Command“ на Mac), чтобы выбрать несколько значений.',
            'status': 'Для работы рассылки, установите статус - "Создана"<br>'
                      'Для прекращения работы рассылки, установите статус - "Завершена"'
        }
        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'}, format='%H-%M'),
            'start_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('user',)


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('user',)
