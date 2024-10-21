from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, help_text="Введите ваше имя")
    last_name = forms.CharField(max_length=30, required=True, help_text="Введите вашу фамилию")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Этот email уже зарегистрирован.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Введите ваше имя")
    last_name = forms.CharField(max_length=30, required=True, help_text="Введите вашу фамилию")
    email = forms.EmailField(required=True, help_text="Введите ваш email")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
