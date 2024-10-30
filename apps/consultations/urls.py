from django.urls import path
from . import views

urlpatterns = [
    # Консультации
    path('info/', views.consultation_info, name='consultation_info'),  # Информация о консультации
    path('order/', views.consultation_order, name='consultation_order'),  # Заказ консультации
    path('payment/<int:consultation_id>/', views.payment, name='payment'),  # URL для оплаты
    path('consultation/<int:consultation_id>/', views.consultation_detail, name='consultation_detail'),
    path('get-available-times/', views.get_available_times, name='get_available_times'),
]