from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.visas.models import VisaAssessment, VisaOrder
from .models import Ticket, TicketComment
from .forms import UserRegisterForm, UserUpdateForm, TicketForm, TicketCommentForm


# Представление для регистрации пользователя
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш аккаунт был создан: {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# Страница личного кабинета
@login_required
def dashboard(request):
    # Заявки на оценку шансов
    assessments = VisaAssessment.objects.filter(user=request.user)

    # Тикеты пользователя
    tickets = Ticket.objects.filter(user=request.user)

    # Заказы пользователя
    orders = VisaOrder.objects.filter(user=request.user)

    return render(request, 'accounts/dashboard.html', {
        'assessments': assessments,
        'tickets': tickets,
        'orders': orders,
    })

# Страница редактирования профиля
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профиль был успешно обновлен!')
            return redirect('dashboard')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('view_tickets')
    else:
        form = TicketForm()
    return render(request, 'accounts/tickets/create_ticket.html', {'form': form})

@login_required
def view_tickets(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'accounts/tickets/view_tickets.html', {'tickets': tickets})


@login_required
def view_ticket_detail(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id, user=request.user)
    comments = TicketComment.objects.filter(ticket=ticket)
    
    if request.method == 'POST':
        form = TicketCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()
            return redirect('view_ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketCommentForm()

    return render(request, 'accounts/tickets/ticket_detail.html', {
        'ticket': ticket,
        'comments': comments,
        'form': form
    })
