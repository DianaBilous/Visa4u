from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ConsultationForm
from .models import Consultation, AvailableSlot
import datetime

# Create your views here.


def consultation_info(request):
    return render(request, 'consultations/consultation_info.html')

@login_required
def consultation_order(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)  # Создаем объект, но не сохраняем сразу
            consultation.user = request.user  # Привязываем пользователя
            consultation.save()  # Сохраняем объект в базу данных
            
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
        
        # Отметим слот как занятый
        slot = AvailableSlot.objects.get(date=consultation.date, time=consultation.time)
        slot.is_booked = True
        slot.save()

        messages.success(request, 'Оплата прошла успешно. Мы свяжемся с вами для подтверждения.')
        return redirect('dashboard')

    return render(request, 'consultations/payment.html', {'consultation': consultation})


@login_required
def consultation_detail(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    return render(request, 'consultations/consultation_detail.html', {'consultation': consultation})

# View для получения доступного времени
@login_required
def get_available_times(request):
    selected_date = request.GET.get('date')
    available_slots = AvailableSlot.objects.filter(date=selected_date, is_booked=False)
    available_times = [slot.time.strftime("%H:%M") for slot in available_slots]
    return JsonResponse({'available_times': available_times})