from django.urls import path
from . import views

urlpatterns = [
    path('usa/', views.visa_usa, name='visa_usa'),
    path('canada/', views.visa_canada, name='visa_canada'),
    path('order/<int:visa_card_id>/', views.order_visa, name='order_visa'),
    
    # ОШ для зарегистрированных пользователей
    path('assessment/<int:visa_type_id>/usa/', views.free_assessment, {'country': 'США'}, name='free_assessment_usa'),
    path('assessment/<int:visa_type_id>/canada/', views.free_assessment, {'country': 'Канада'}, name='free_assessment_canada'),

    # ОШ для незарегистрированных пользователей
    path('assessment/<int:visa_type_id>/guest/usa/', views.free_assessment_guest, {'country': 'США'}, name='free_assessment_guest_usa'),
    path('assessment/<int:visa_type_id>/guest/canada/', views.free_assessment_guest, {'country': 'Канада'}, name='free_assessment_guest_canada'),
]
