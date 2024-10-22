from django import forms
from .models import VisaAssessment, DocumentUpload
from .constants import COUNTRY_CASES 

class VisaAssessmentForm(forms.ModelForm):
    class Meta:
        model = VisaAssessment
        fields = [
            'age', 'citizenship', 'residence', 'marital_status', 'travel_purpose', 'who_pays',
            'previous_visa', 'previous_trips', 'visa_denial', 'relatives_in_country', 'occupation',
            'work_experience', 'salary', 'visited_countries', 'deported', 'illegal_stay', 'additional_info',
            'email', 'phone', 'name'
        ]

    def __init__(self, *args, **kwargs):
        country = kwargs.pop('country', 'США')  # Для США передаем значение по умолчанию
        super().__init__(*args, **kwargs)

        # Если страна - Канада, используем падежи
        if country == 'Канада':
            country_cases = COUNTRY_CASES.get('Канада', {})
            country_prepositional = country_cases.get('prepositional', 'Канаде')  # Предложный падеж
        else:
        # Для США оставляем название страны неизменным
            country_prepositional = country

        # Динамически изменяем текст меток для полей
        self.fields['previous_trips'].label = f"Были ли вы ранее в {country_prepositional}?"
        self.fields['relatives_in_country'].label = f"Есть ли у вас родственники или друзья в {country_prepositional}?"

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = DocumentUpload
        fields = ['document_type', 'file']
