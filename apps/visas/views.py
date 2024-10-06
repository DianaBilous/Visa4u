from django.contrib.auth.decorators import login_required
from .constants import COUNTRY_CASES
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from .forms import VisaAssessmentForm
from .models import Country, VisaType, VisaRequirement, VisaOrder, FAQ

# Create your views here.

# Визы в США
def visa_usa(request):
    # Получаем страну США из базы данных
    country = get_object_or_404(Country, name="США")
    
    # Получаем типы виз, связанные с этой страной
    visa_types = VisaType.objects.filter(country=country)
    
    # Получаем требования к визам
    visa_requirements = VisaRequirement.objects.filter(visa_type__country=country)
    
    # Получаем FAQ по визам
    faq = FAQ.objects.filter(visa_type__country=country)
    
    return render(request, 'visas/visa_usa.html', {
        'visa_types': visa_types,
        'visa_requirements': visa_requirements,
        'faq': faq,
        'usa_visa_type': visa_types.first()  # Для примера привязываем первую визу к бесплатной оценке шансов и заказу визы
    })

# Визы в Канаду
def visa_canada(request):
    # Получаем страну Канада из базы данных
    country = get_object_or_404(Country, name="Канада")
    
    # Получаем типы виз, связанные с этой страной
    visa_types = VisaType.objects.filter(country=country)
    
    # Получаем требования к визам
    visa_requirements = VisaRequirement.objects.filter(visa_type__country=country)
    
    # Получаем FAQ по визам
    faq = FAQ.objects.filter(visa_type__country=country)
    
    return render(request, 'visas/visa_canada.html', {
        'visa_types': visa_types,
        'visa_requirements': visa_requirements,
        'faq': faq,
        'canada_visa_type': visa_types.first()  # Для примера привязываем первую визу к бесплатной оценке шансов и заказу визы
    })

# Представление для зарегистрированных пользователей
def free_assessment(request, visa_type_id, country):
    visa_type = get_object_or_404(VisaType, id=visa_type_id)

    # Получаем падежи для Канады, если страна - Канада
    country_cases = COUNTRY_CASES.get(country, {})
    country_accusative = country_cases.get('accusative', country)  # Винительный падеж
    country_prepositional = country_cases.get('prepositional', country)  # Предложный падеж

    if request.method == 'POST':
        form = VisaAssessmentForm(request.POST, country=country_prepositional)
        if form.is_valid():
            assessment = form.save(commit=False)
            if request.user.is_authenticated:
                assessment.user = request.user  # Привязываем к пользователю, если залогинен
            assessment.country = country
            assessment.save()

            # Отправляем email уведомление
            send_mail(
                f'Ваш запрос на оценку шансов для визы в {country_accusative} принят',
                f'Спасибо за ваш запрос. Вы можете отслеживать статус вашей заявки в личном кабинете. Мы также уведомим вас по email, когда будет готов ответ по визе в {country_prepositional}.',
                'noreply@visa4u.com',
                [assessment.email],
                fail_silently=False,
            )

            return redirect('dashboard' if request.user.is_authenticated else 'thanks')
    else:
        form = VisaAssessmentForm(country=country_prepositional)

    return render(request, 'visas/free_assessment.html', {
        'form': form,
        'visa_type': visa_type,
        'country_accusative': country_accusative,
        'country_prepositional': country_prepositional,
    })

# Представление для незарегистрированных пользователей
def free_assessment_guest(request, visa_type_id, country):
    visa_type = get_object_or_404(VisaType, id=visa_type_id)

    # Получаем падежи для Канады, если страна - Канада
    country_cases = COUNTRY_CASES.get(country, {})
    country_accusative = country_cases.get('accusative', country)  # Винительный падеж
    country_prepositional = country_cases.get('prepositional', country)  # Предложный падеж

    if request.method == 'POST':
        form = VisaAssessmentForm(request.POST, country=country_prepositional)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.country = country
            assessment.save()

            # Отправляем email уведомление
            send_mail(
                f'Ваш запрос на оценку шансов для визы в {country_accusative} принят',
                f'Спасибо за ваш запрос. Мы свяжемся с вами по указанному email, когда будет готов ответ по визе в {country_prepositional}.',
                'noreply@visa4u.com',
                [assessment.email],
                fail_silently=False,
            )

            return redirect('thanks')
    else:
        form = VisaAssessmentForm(country=country_prepositional)

    return render(request, 'visas/free_assessment_guest.html', {
        'form': form,
        'visa_type': visa_type,
        'country_accusative': country_accusative,
        'country_prepositional': country_prepositional,
    })


@login_required
def order_visa(request, visa_type_id):
    # Получаем тип визы
    visa_type = get_object_or_404(VisaType, id=visa_type_id)

    if request.method == 'POST':
        # Создаем заказ
        order = VisaOrder.objects.create(
            user=request.user,
            visa_type=visa_type,
            price=visa_type.price,  # Предполагаем, что в модели VisaType есть поле price
            status='Pending'
        )
        # Перенаправляем пользователя на его личный кабинет или другую страницу
        return redirect('dashboard')  # Или страница подтверждения заказа
    
    return render(request, 'visas/order_visa.html', {'visa_type': visa_type})
