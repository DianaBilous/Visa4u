from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ConsultationForm
from .models import Consultation, AvailableSlot

# Create your views here.

# Представление для отображения информации о консультации
def consultation_info(request):
    return render(request, 'consultations/consultation_info.html')

@login_required
def consultation_order(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)  # Создаем объект консультации, но не сохраняем сразу
            consultation.user = request.user  # Привязываем консультацию к текущему пользователю
            
            # Получаем выбранные дату и время из формы
            selected_date = form.cleaned_data.get('date')
            selected_time = form.cleaned_data.get('time')
            
            # Проверяем, есть ли свободный слот с указанной датой и временем
            slot = get_object_or_404(AvailableSlot, date=selected_date, time=selected_time, is_booked=False)
            
            # Помечаем слот как занятый
            slot.is_booked = True
            slot.save()

            # Сохраняем консультацию
            consultation.save()
            
            # Перенаправляем пользователя на страницу оплаты
            return redirect('payment', consultation_id=consultation.id)  # Передаем ID для оплаты
    else:
        form = ConsultationForm()

    return render(request, 'consultations/consultation_order.html', {'form': form})

def payment(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    
    # Логика для обработки платежа (здесь нужно интегрировать API платежной системы)
    if request.method == 'POST':
        # Заглушка: представим, что платеж прошел успешно
        consultation.status = 'paid'
        consultation.save()
        
        # Проверяем, что слот существует, перед тем как отметить его как занятый
        try:
            slot = AvailableSlot.objects.get(date=consultation.date, time=consultation.time)
            slot.is_booked = True
            slot.save()
        except AvailableSlot.DoesNotExist:
            messages.error(request, 'Выбранный слот больше недоступен. Пожалуйста, выберите другой слот.')
            return redirect('consultation_order')

        messages.success(request, 'Оплата прошла успешно. Мы свяжемся с вами для подтверждения.')
        return redirect('dashboard')

    return render(request, 'consultations/payment.html', {'consultation': consultation})

# Отображение деталей консультации
@login_required
def consultation_detail(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    return render(request, 'consultations/consultation_detail.html', {'consultation': consultation})

# View для получения доступного времени
@login_required
def get_available_times(request):
    selected_date = request.GET.get('date')
    print("Получена дата:", selected_date)  # Отладка: проверка полученной даты
    
    if selected_date:
        selected_date = parse_date(selected_date)
        print("Обработанная дата:", selected_date)  # Отладка: проверка преобразования
        
        today = timezone.now().date()
        if selected_date < today:
            print("Дата в прошлом, слоты недоступны.")
            return JsonResponse({'available_times': []})

        available_slots = AvailableSlot.objects.filter(date=selected_date, is_booked=False).order_by('time')
        available_times = [slot.time.strftime('%H:%M') for slot in available_slots]
        
        print("Доступные слоты:", available_times)  # Отладка: проверка извлеченных слотов
        return JsonResponse({'available_times': available_times})
    
    print("Дата не выбрана или некорректна.")
    return JsonResponse({'available_times': []})