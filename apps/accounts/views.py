from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from apps.visas.models import VisaAssessment, VisaOrder
from apps.consultations.models import Consultation
from .forms import UserRegisterForm, UserUpdateForm, UserLoginForm, CustomPasswordChangeForm


# Представление для регистрации пользователя
def register(request):
    # Если пользователь уже вошёл в систему, перенаправляем
    if request.user.is_authenticated:
        return redirect('dashboard')  # Перенаправляем на личный кабинет

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # Устанавливаем бэкенд для аутентификации
            login(request, user)  # Автоматически авторизуем пользователя
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш аккаунт был создан: {username} и вы вошли в систему!')
            return redirect('dashboard')  # Перенаправляем на личный кабинет
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

# Представление для логина
def user_login(request):
    # Если пользователь уже вошёл в систему, перенаправляем
    if request.user.is_authenticated:
        return redirect('dashboard')  # Перенаправляем на личный кабинет
    
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Перенаправление на главную страницу
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('password_change_done')

# Представление для отображения информации о заказе
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(VisaOrder, id=order_id, user=request.user)

    if request.method == 'POST':
        if 'passport_photo' in request.FILES:
            passport_photo = request.FILES['passport_photo']
            email = request.POST.get('email')
            # Логика для сохранения документов
            order.required_documents.add(passport_photo)
            # Дополнительные действия (например, уведомление менеджера)
            messages.success(request, "Документы успешно отправлены.")
            return redirect('order_detail', order_id=order.id)
    return render(request, 'accounts/order_detail.html', {'order': order})

# Представление для отображения информации о заявке на оценку шансов
@login_required
def assessment_detail(request, assessment_id):
    assessment = get_object_or_404(VisaAssessment, id=assessment_id, user=request.user)
    return render(request, 'accounts/assessment_detail.html', {'assessment': assessment})
