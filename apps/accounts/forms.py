from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Электронная почта",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите вашу электронную почту'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="Имя",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Фамилия",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите вашу фамилию'
        })
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'Имя пользователя',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя пользователя'
            }),
        }

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
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="Имя",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Фамилия",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите вашу фамилию'
        })
    )
    email = forms.EmailField(
        required=True,
        label="Электронная почта",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Имя пользователя',  # Устанавливаем метку для username
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя пользователя'
            }),
        }

# Форма логина
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",  # Устанавливаем метку на русском
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'})
    )
    password = forms.CharField(
        label="Пароль",  # Устанавливаем метку на русском
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Старый пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите старый пароль'
        })
    )
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите новый пароль'
        }),
        help_text="Ваш пароль должен содержать минимум 8 символов, не быть слишком простым и не совпадать с другими личными данными."
    )
    new_password2 = forms.CharField(
        label="Подтверждение нового пароля",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите новый пароль'
        })
    )
