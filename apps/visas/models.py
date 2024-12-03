from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Country(models.Model):
    """Модель для хранения стран"""
    name = models.CharField(max_length=100, verbose_name="Название страны")  # "США", "Канада"
    
    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name


class VisaType(models.Model):
    """Модель для хранения типов виз"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='visa_types', verbose_name="Страна")
    name = models.CharField(max_length=100, verbose_name="Тип визы")  # "Туристическая", "Студенческая"
    description = models.TextField(verbose_name="Описание")
    
    class Meta:
        verbose_name = "Тип визы"
        verbose_name_plural = "Типы виз"

    def __str__(self):
        return f"{self.name} ({self.country.name})"


class VisaRequirement(models.Model):
    """Модель для хранения требований к визам"""
    visa_type = models.ForeignKey(VisaType, on_delete=models.CASCADE, related_name='requirements', verbose_name="Тип визы")
    requirement = models.TextField(verbose_name="Требование") 
    
    class Meta:
        verbose_name = "Требование для визы"
        verbose_name_plural = "Требования для виз"

    def __str__(self):
        return f"Requirement for {self.visa_type.name}"


class VisaDocument(models.Model):
    """Модель для хранения документов, необходимых для виз"""
    visa_type = models.ForeignKey(VisaType, on_delete=models.CASCADE, related_name='documents', verbose_name="Тип визы")
    document_name = models.CharField(max_length=200, verbose_name="Название документа") # Название документа

    class Meta:
        verbose_name = "Документ для визы"
        verbose_name_plural = "Документы для виз"

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
    phone = PhoneNumberField(unique=True, blank=False, null=False, verbose_name="Номер телефона")
    name = models.CharField(max_length=100, verbose_name="Имя")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received', verbose_name="Статус заявки")
    result = models.TextField(null=True, blank=True, verbose_name="Результат оценки")
    recommendations = models.TextField(null=True, blank=True, verbose_name="Рекомендации")

    class Meta:
        verbose_name = "Запрос на бесплатную оценку шансов"
        verbose_name_plural = "Запросы на бесплатную оценку шансов"

    def __str__(self):
        return f"{self.name} - {self.email}"
    
class VisaCard(models.Model):
    """Модель для хранения карточек заказа"""
    title = models.CharField(max_length=200, verbose_name="Название визы")
    price = models.CharField(max_length=50, verbose_name="Цена")
    description = models.TextField(verbose_name="Описание")
    consular_fee = models.BooleanField(default=False, verbose_name="Включен ли консульский сбор")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Страна", default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Визовая карточка"
        verbose_name_plural = "Визовые карточки"


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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visa_orders', verbose_name="Пользователь")
    visa_card = models.ForeignKey(VisaCard, on_delete=models.CASCADE, verbose_name="Виза", null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    comments = models.TextField(blank=True, null=True, verbose_name="Комментарии")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='paid', verbose_name="Статус")
    assigned_manager = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_orders', verbose_name="Менеджер"
    )
    required_documents = models.ManyToManyField(VisaDocument, blank=True, verbose_name="Требуемые документы")
    interview_date = models.DateField(blank=True, null=True, verbose_name="Дата собеседования")
    interview_time = models.TimeField(blank=True, null=True, verbose_name="Время собеседования")
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name="Страна подачи")

    class Meta:
        verbose_name = "Заказ на визу"
        verbose_name_plural = "Заказы на визы"
        ordering = ['-order_date']

    def __str__(self):
        return f"Заказ {self.visa_card.title} от {self.user.username}"

    def is_completed(self):
        """Проверяет завершённость заказа."""
        return self.status == 'completed'


class FAQ(models.Model):
    """Модель для хранения часто задаваемых вопросов"""
    visa_type = models.ForeignKey(VisaType, on_delete=models.CASCADE, related_name='faqs', verbose_name="Тип визы")
    question = models.CharField(max_length=300, verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")

    class Meta:
        verbose_name = "Часто задаваемый вопрос"
        verbose_name_plural = "Часто задаваемые вопросы"

    def __str__(self):
        return f"FAQ: {self.question} for {self.visa_type.name}"


class DocumentUpload(models.Model):
    order = models.ForeignKey(VisaOrder, on_delete=models.CASCADE, related_name='uploaded_documents', verbose_name="Заказ")
    file = models.FileField(upload_to='documents/', verbose_name="Файл")
    document_type = models.CharField(max_length=255, verbose_name="Тип документа")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Загруженные документы"

    def __str__(self):
        return f"Документ для заказа {self.order.user.username} - {self.document_type}"
