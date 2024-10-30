from django import forms
from .models import Consultation

class ConsultationForm(forms.ModelForm):
    phone = forms.CharField(max_length=15, label="Телефон", required=True,
                            widget=forms.TextInput(attrs={'placeholder': 'Введите ваш номер телефона'}))
    email = forms.EmailField(label="Электронная почта", required=True,
                             widget=forms.EmailInput(attrs={'placeholder': 'Введите вашу электронную почту'}))

    class Meta:
        model = Consultation
        fields = ['full_name', 'topic', 'date', 'time', 'additional_info', 'phone', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Введите ваше полное имя'}),
            'topic': forms.Select(choices=[
                ('Виза в США', 'Получение визы в США'),
                ('Виза в Канаду', 'Получение визы в Канаду'),
                ('Шенгенская виза', 'Получение шенгенской визы'),
                ('Документы', 'Подготовка документов'),
                ('Другие вопросы', 'Другие вопросы')
            ]),
            'additional_info': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Дополнительная информация (необязательно)'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'datepicker'}),
            'time': forms.Select(attrs={'class': 'form-control', 'id': 'timepicker'}),
        }

# class TimeSlot(models.Model):
#     date = models.DateField(verbose_name="Дата")
#     time = models.TimeField(verbose_name="Время")
#     is_booked = models.BooleanField(default=False, verbose_name="Забронирован")

#     def __str__(self):
#         return f"{self.date} {self.time} {'(Занято)' if self.is_booked else '(Свободно)'}"