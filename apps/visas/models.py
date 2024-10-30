from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Country(models.Model):
    """Модель для хранения стран"""
    name = models.CharField(max_length=100)  # "США", "Канада"
    
    def __str__(self):
        return self.name


class VisaType(models.Model):
    """Модель для хранения типов виз"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='visa_types')
    name = models.CharField(max_length=100)  # "Туристическая", "Студенческая"
    description = models.TextField()  # Описание типа визы
    
    def __str__(self):
        return f"{self.name} ({self.country.name})"


class VisaRequirement(models.Model):
    """Модель для хранения требований к визам"""
    visa_type = models.ForeignKey(VisaType, on_delete=models.CASCADE, related_name='requirements')
    requirement = models.TextField()  # Текст с требованием
    
    def __str__(self):
        return f"Requirement for {self.visa_type.name}"


class VisaDocument(models.Model):
    """Модель для хранения документов, необходимых для виз"""
    visa_type = models.ForeignKey(VisaType, on_delete=models.CASCADE, related_name='documents')
    document_name = models.CharField(max_length=200)  # Название документа

    def __str__(self):
        return f"Document: {self.document_name} for {self.visa_type.name}"
 
class VisaAssessment(models.Model):
    """Модель для хранения запросов на бесплатную оценку шансов"""
    
    YES_NO_CHOICES = [
        ('yes', 'Да'),
        ('no', 'Нет'),
    ]
    
    STATUS_CHOICES = [
        ('received', 'Получена'),
        ('processing', 'В работе'),
        ('done', 'Готова'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    age = models.IntegerField(verbose_name="Ваш возраст")
    citizenship = models.CharField(max_length=100, verbose_name="Ваше гражданство")
    residence = models.CharField(max_length=255, verbose_name="В какой стране и городе Вы проживаете")
    marital_status = models.CharField(max_length=50, verbose_name="Ваш семейный статус")
    travel_purpose = models.CharField(max_length=100, verbose_name="Цель поездки")
    who_pays = models.CharField(max_length=100, verbose_name="Кто оплачивает Вашу поездку")
    previous_visa = models.CharField(max_length=100, verbose_name="Была ли у Вас ранее туристическая виза")
    previous_trips = models.TextField(
        verbose_name="Были ли Вы ранее в этой стране", 
        help_text="Если да, то уточните в каком статусе и продолжительность поездки"
    )
    visa_denial = models.CharField(max_length=3, choices=YES_NO_CHOICES, verbose_name="Отказывали ли Вам когда-либо в визе")
    relatives_in_country = models.TextField(verbose_name="Есть ли родственники или друзья в этой стране")
    occupation = models.CharField(max_length=100, verbose_name="Ваша текущая сфера деятельности")
    work_experience = models.CharField(max_length=100, verbose_name="Срок работы в текущей компании")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Заработная плата (руб/мес)")
    visited_countries = models.TextField(verbose_name="Зарубежные страны, которые вы посетили за последние 5 лет")
    deported = models.CharField(max_length=3, choices=YES_NO_CHOICES, verbose_name="Были ли Вы депортированы из других стран")
    illegal_stay = models.CharField(max_length=3, choices=YES_NO_CHOICES, verbose_name="Находились ли Вы когда-либо незаконно на территории другой страны")
    additional_info = models.TextField(blank=True, null=True, verbose_name="Дополнительная информация")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    name = models.CharField(max_length=100, verbose_name="Имя")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received', verbose_name="Статус заявки")
    result = models.TextField(null=True, blank=True, verbose_name="Результат оценки")
    recommendations = models.TextField(null=True, blank=True, verbose_name="Рекомендации")

    def __str__(self):
        return f"{self.name} - {self.email}"

class VisaOrder(models.Model):
    """Модель для хранения заказов на визы"""

    STATUS_CHOICES = [
        ('paid', 'Заказ оплачен'),
        ('manager_assigned', 'Менеджер назначен'),
        ('awaiting_documents', 'Ожидание документов'),
        ('awaiting_interview', 'Ожидание записи'),
        ('scheduled', 'Записан на собеседование'),
        ('approved', 'Виза одобрена'),
        ('denied', 'Отказ'),
        ('completed', 'Заявка закрыта'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visa_orders')
    visa_type = models.ForeignKey(VisaType, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='paid', verbose_name="Статус заказа")
    assigned_manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_orders')
    required_documents = models.ManyToManyField(VisaDocument, blank=True)

    def __str__(self):
        return f"Visa order for {self.visa_type.name} by {self.user.username}"


class FAQ(models.Model):
    """Модель для хранения часто задаваемых вопросов"""
    visa_type = models.ForeignKey(VisaType, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=300)
    answer = models.TextField()

    def __str__(self):
        return f"FAQ: {self.question} for {self.visa_type.name}"


class DocumentUpload(models.Model):
    order = models.ForeignKey(VisaOrder, on_delete=models.CASCADE, related_name='uploaded_documents')
    file = models.FileField(upload_to='documents/')
    document_type = models.CharField(max_length=255, verbose_name="Тип документа")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Документ для заказа {self.order.user.username} - {self.document_type}"
