from django.shortcuts import render
from django.http import HttpResponse

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

        # Здесь можно будет добавить логику обработки, например, отправку email или сохранение в базу
        print(f'Сообщение от {name} ({email}): {message}')

        return HttpResponse("Спасибо за ваше сообщение!")
    return HttpResponse("Ошибка: неверный запрос.")