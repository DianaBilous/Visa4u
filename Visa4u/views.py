from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages


def home_page(request):
    return render(request, 'index.html')

def about_page(request):
    return render(request, 'about.html') 

def contact_page(request):
    return render(request, 'contacts.html')

def contact_submit(request):
    if request.method == 'POST':
        # Обрабатываем данные из формы
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        try:
            # Отправка Email
            send_mail(
                subject=f"Новое сообщение от {name}",
                message=f"Сообщение от {name} ({email}):\n\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            # Добавление сообщения об успешной отправке
            messages.success(request, "Ваше сообщение отправлено! Мы свяжемся с вами по email.")
        except Exception as e:
            # Добавление сообщения об ошибке
            messages.error(request, f"Произошла ошибка при отправке сообщения: {e}")

        # Перенаправление обратно на страницу контактов
        return redirect('contact')  # 'contact' — имя URL для страницы контактов

    # Если запрос не POST
    messages.error(request, "Неверный запрос.")
    return redirect('contact')

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)