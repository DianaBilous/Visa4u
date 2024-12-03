from django import forms
from django.utils import timezone
from .models import Consultation
from phonenumber_field.formfields import PhoneNumberField

class ConsultationForm(forms.ModelForm):
    phone = PhoneNumberField(
        max_length=17, 
        label="Телефон", 
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите ваш номер телефона',
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        label="Электронная почта", 
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Введите вашу электронную почту',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Consultation
        fields = ['full_name', 'topic', 'date', 'time', 'additional_info', 'phone', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Введите ваше полное имя',
                'class': 'form-control'
            }),
            'topic': forms.Select(choices=[
                ('Виза в США', 'Получение визы в США'),
                ('Виза в Канаду', 'Получение визы в Канаду'),
                ('Шенгенская виза', 'Получение шенгенской визы'),
                ('Документы', 'Подготовка документов'),
                ('Другие вопросы', 'Другие вопросы')
            ], attrs={'class': 'form-control'}),
            'additional_info': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Дополнительная информация (необязательно)',
                'class': 'form-control'
            }),
            
            # Виджет для выбора даты с ограничением на выбор прошлых дат
            'date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control', 
                'id': 'datepicker',
                'min': timezone.now().date().strftime('%Y-%m-%d')  # Установка минимальной даты на сегодняшнюю
            }),
            
            # Виджет для выбора времени - пустой Select, который будет заполняться через AJAX
            'time': forms.Select(attrs={'class': 'form-control', 'id': 'timepicker'}),
        }

# class TimeSlot(models.Model):
#     date = models.DateField(verbose_name="Дата")
#     time = models.TimeField(verbose_name="Время")
#     is_booked = models.BooleanField(default=False, verbose_name="Забронирован")

#     def __str__(self):
#         return f"{self.date} {self.time} {'(Занято)' if self.is_booked else '(Свободно)'}"