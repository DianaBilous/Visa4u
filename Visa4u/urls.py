"""
URL configuration for Visa4u project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import home_page, about_page, contact_page, contact_submit
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('visas/', include('apps.visas.urls')),  # Подключаем маршруты из приложения visas
    path('about/', about_page, name='about'),  # URL для страницы "О нас"
    path('contacts/', contact_page, name='contact'),  # URL для страницы "Контакты"
    path('contacts/submit/', contact_submit, name='contact_submit'),  # URL для отправки формы
    path('accounts/', include('apps.accounts.urls')),  # Подключаем маршруты из приложения accounts
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('consultations/', include('apps.consultations.urls')), # Консультации
]
