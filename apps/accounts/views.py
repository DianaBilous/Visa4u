from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from apps.visas.models import VisaAssessment, VisaOrder, Consultation
from .forms import UserRegisterForm, UserUpdateForm


# Представление для регистрации пользователя
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически авторизуем пользователя
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш аккаунт был создан: {username} и вы вошли в систему!')
            return redirect('home')  # Перенаправление на главную страницу
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# Страница личного кабинета
@login_required
def dashboard(request):
    # Заявки на оценку шансов
    assessments = VisaAssessment.objects.filter(user=request.user)

    # Заказы пользователя
    orders = VisaOrder.objects.filter(user=request.user)

    # Консультации пользователя
    consultations = Consultation.objects.filter(user=request.user)

    return render(request, 'accounts/dashboard.html', {
        'assessments': assessments,
        'orders': orders,
        'consultations': consultations,  # Добавляем консультации
    })

# Страница редактирования профиля
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)  # Обработка файлов
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профиль был успешно обновлен!')
            return redirect('dashboard')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})

def chat_view(request):
    return render(request, 'accounts/chat.html')
