# core/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone
from datetime import date
import logging
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)

class StaffMember(models.Model):
    """Сотрудник компании (общая информация)"""
    POSITION_CHOICES = [
        ('agent', 'Страховой агент'),
        ('manager', 'Менеджер'),
        ('director', 'Директор'),
        ('accountant', 'Бухгалтер'),
        ('lawyer', 'Юрист'),
        ('hr', 'HR-специалист'),
        ('it', 'IT-специалист'),
        ('marketing', 'Маркетолог'),
    ]
    
    full_name = models.CharField("ФИО", max_length=200)
    position = models.CharField("Должность", max_length=50, choices=POSITION_CHOICES)
    department = models.CharField("Отдел", max_length=100, blank=True)
    phone = models.CharField(
        "Телефон",
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+375\s\(\d{2}\)\s\d{3}-\d{2}-\d{2}$',
                message='Телефон должен быть в формате +375 (29) XXX-XX-XX'
            )
        ]
    )
    email = models.EmailField("Email")
    photo = models.ImageField("Фото", upload_to='staff/', null=True, blank=True)
    bio = models.TextField("Краткая биография", blank=True)
    hire_date = models.DateField("Дата приёма на работу")
    is_active = models.BooleanField("Работает", default=True)
    order = models.IntegerField("Порядок отображения", default=0)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ['order', 'full_name']

    def __str__(self):
        return f"{self.full_name} - {self.get_position_display()}"
    
class Branch(models.Model):
    """Филиал страховой компании"""
    name = models.CharField("Название филиала", max_length=200)
    address = models.TextField("Адрес")
    phone = models.CharField(
        "Телефон",
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+375\s\(\d{2}\)\s\d{3}-\d{2}-\d{2}$',
                message='Телефон должен быть в формате +375 (29) XXX-XX-XX'
            )
        ]
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Филиал"
        verbose_name_plural = "Филиалы"
        ordering = ['name']

    def __str__(self):
        return self.name


class InsuranceType(models.Model):
    name = models.CharField("Название вида страхования", max_length=200)
    description = models.TextField("Описание", blank=True)
    commission_percent = models.DecimalField(
        "Процент комиссии агента",
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    tariff_rate = models.DecimalField(  # <-- ДОБАВИТЬ ЭТО ПОЛЕ
        "Тарифная ставка (%)",
        max_digits=5,
        decimal_places=2,
        default=10.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    tariff_rate = models.DecimalField(
        "Тарифная ставка (%)",
        max_digits=5,
        decimal_places=2,
        default=10.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"{self.name} (тариф: {self.tariff_rate}%)"
    
    class Meta:
        verbose_name = _("Вид страхования")
        verbose_name_plural = _("Виды страхования")
    



class Client(models.Model):
    """Клиент страховой компании"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        null=True,
        blank=True
    )
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    middle_name = models.CharField("Отчество", max_length=100, blank=True)
    address = models.TextField("Адрес")
    phone = models.CharField(
        "Телефон",
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+375\s\(\d{2}\)\s\d{3}-\d{2}-\d{2}$',
                message='Телефон должен быть в формате +375 (29) XXX-XX-XX'
            )
        ]
    )
    email = models.EmailField("Email")
    birth_date = models.DateField("Дата рождения")
    passport_number = models.CharField("Номер паспорта", max_length=20, unique=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.age() < 18:
            raise ValidationError("Клиенту должно быть 18 лет или больше")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class InsuranceAgent(models.Model):
    """Страховой агент"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        null=True,
        blank=True
    )
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    middle_name = models.CharField("Отчество", max_length=100, blank=True)
    address = models.TextField("Адрес")
    phone = models.CharField(
        "Телефон",
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+375\s\(\d{2}\)\s\d{3}-\d{2}-\d{2}$',
                message='Телефон должен быть в формате +375 (29) XXX-XX-XX'
            )
        ]
    )
    birth_date = models.DateField("Дата рождения")
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='agents',
        verbose_name="Филиал"
    )
    hire_date = models.DateField("Дата приёма на работу", default=date.today)
    is_active = models.BooleanField("Активен", default=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Страховой агент"
        verbose_name_plural = "Страховые агенты"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name} - {self.branch.name}"

    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.age() < 18:
            raise ValidationError("Агенту должно быть 18 лет или больше")

    def save(self, *args, **kwargs):
        self.clean()
        logger.info(f"Сохранён страховой агент: {self}")
        super().save(*args, **kwargs)


class InsuredObject(models.Model):
    """Объект страхования"""
    OBJECT_TYPES = [
        ('car', 'Автомобиль'),
        ('property', 'Имущество'),
        ('health', 'Здоровье'),
        ('life', 'Жизнь'),
        ('travel', 'Путешествия'),
    ]
    
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='insured_objects',
        verbose_name="Клиент"
    )
    object_type = models.CharField("Тип объекта", max_length=20, choices=OBJECT_TYPES)
    description = models.TextField("Описание")
    value = models.DecimalField(
        "Страховая стоимость",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Объект страхования"
        verbose_name_plural = "Объекты страхования"

    def __str__(self):
        return f"{self.get_object_type_display()} - {self.client}"


class InsuranceContract(models.Model):
    """Договор страхования"""
    STATUS_CHOICES = [
        ('active', 'Активен'),
        ('expired', 'Истёк'),
        ('cancelled', 'Расторгнут'),
    ]
    
    
    contract_number = models.CharField("Номер договора", max_length=50, unique=True)
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='contracts',
        verbose_name="Клиент"
    )
    agent = models.ForeignKey(
        StaffMember,
        on_delete=models.CASCADE,
        related_name='contracts',
        verbose_name="Страховой агент",
        limit_choices_to={'position': 'agent'}  # Только сотрудники с должностью "Страховой агент"
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='contracts',
        verbose_name="Филиал"
    )
    insurance_type = models.ForeignKey(
        InsuranceType,
        on_delete=models.CASCADE,
        related_name='contracts',
        verbose_name="Вид страхования"
    )
    insured_object = models.ForeignKey(
        InsuredObject,
        on_delete=models.CASCADE,
        related_name='contracts',
        verbose_name="Объект страхования",
        null=True,
        blank=True
    )
    insurance_sum = models.DecimalField(
        "Страховая сумма",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    tariff_rate = models.DecimalField(
        "Тарифная ставка (%)",
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    final_payment = models.DecimalField(
        "Итоговый платёж с учётом скидки",
        max_digits=12,
        decimal_places=2,
        default=0,
        null=True,
        blank=True
    )
    start_date = models.DateField("Дата начала")
    end_date = models.DateField("Дата окончания")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Договор страхования"
        verbose_name_plural = "Договоры страхования"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.contract_number} - {self.client}"

    def insurance_payment(self):
        return self.insurance_sum * self.tariff_rate / 100

    def agent_commission(self):
        return self.insurance_payment() * self.insurance_type.commission_percent / 100

    def save(self, *args, **kwargs):
        if not self.contract_number:
            import random
            import string
            self.contract_number = ''.join(random.choices(string.digits, k=12))
        super().save(*args, **kwargs)


class PromoCode(models.Model):
    """Промокод/купон"""
    code = models.CharField("Код промокода", max_length=50, unique=True)
    discount_percent = models.DecimalField(
        "Скидка (%)",
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    description = models.TextField("Описание", blank=True)
    valid_from = models.DateTimeField("Действует с")
    valid_to = models.DateTimeField("Действует до")
    is_active = models.BooleanField("Активен", default=True)
    max_uses = models.IntegerField("Максимальное использование", default=1)
    used_count = models.IntegerField("Количество использований", default=0)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} ({self.discount_percent}%)"

    def is_valid(self):
        now = timezone.now()
        return (self.is_active and 
                self.valid_from <= now <= self.valid_to and
                self.used_count < self.max_uses)


class Review(models.Model):
    """Отзыв клиента"""
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Клиент",
        unique=True  
    )
    rating = models.IntegerField(
        "Оценка",
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    text = models.TextField("Текст отзыва")
    is_published = models.BooleanField("Опубликован", default=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Отзыв {self.client} - {self.rating}/5"


class FAQ(models.Model):
    """Часто задаваемые вопросы"""
    question = models.TextField("Вопрос")
    answer = models.TextField("Ответ")
    is_published = models.BooleanField("Опубликован", default=True)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"
        ordering = ['-created_at']

    def __str__(self):
        return self.question[:50]


class Vacancy(models.Model):
    """Вакансия"""
    title = models.CharField("Название вакансии", max_length=200)
    description = models.TextField("Описание")
    requirements = models.TextField("Требования")
    salary_from = models.DecimalField(
        "Зарплата от",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    salary_to = models.DecimalField(
        "Зарплата до",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    location = models.CharField("Местоположение", max_length=200)
    is_active = models.BooleanField("Активна", default=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class CompanyInfo(models.Model):
    """Информация о компании"""
    name = models.CharField("Название компании", max_length=200)
    short_description = models.TextField("Краткое описание")
    full_description = models.TextField("Полное описание")
    foundation_year = models.IntegerField("Год основания")
    ceo_name = models.CharField("Имя директора", max_length=200)
    employees_count = models.IntegerField("Количество сотрудников", default=0)
    logo = models.ImageField("Логотип", upload_to='logos/', null=True, blank=True)
    video_url = models.URLField("URL видео", blank=True)
    legal_address = models.TextField("Юридический адрес")
    actual_address = models.TextField("Фактический адрес")
    inn = models.CharField("ИНН", max_length=20)
    kpp = models.CharField("КПП", max_length=20, blank=True)
    ogrn = models.CharField("ОГРН", max_length=20)
    bank_name = models.CharField("Банк", max_length=200)
    bank_account = models.CharField("Расчётный счёт", max_length=20)
    bik = models.CharField("БИК", max_length=20)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Информация о компании"
        verbose_name_plural = "Информация о компании"

    def __str__(self):
        return self.name


class Contact(models.Model):
    """Контактное лицо компании"""
    company = models.ForeignKey(
        CompanyInfo,
        on_delete=models.CASCADE,
        related_name='contacts',
        verbose_name="Компания"
    )
    full_name = models.CharField("ФИО", max_length=200)
    position = models.CharField("Должность", max_length=200)
    phone = models.CharField("Телефон", max_length=20)
    email = models.EmailField("Email")
    photo = models.ImageField("Фото", upload_to='contacts/', null=True, blank=True)
    responsibilities = models.TextField("Выполняемые работы")
    order = models.IntegerField("Порядок отображения", default=0)

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ['order', 'full_name']

    def __str__(self):
        return f"{self.full_name} - {self.position}"


class News(models.Model):
    """Новости компании"""
    title = models.CharField("Заголовок", max_length=200)
    content = models.TextField("Содержание")
    short_description = models.CharField("Краткое описание", max_length=300)
    image = models.ImageField("Изображение", upload_to='news/', null=True, blank=True)
    is_published = models.BooleanField("Опубликовано", default=True)
    created_at = models.DateTimeField("Дата публикации", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class CompanyHistory(models.Model):
    """История компании по годам"""
    year = models.IntegerField("Год")
    title = models.CharField("Заголовок события", max_length=200)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to='history/', null=True, blank=True)
    order = models.IntegerField("Порядок", default=0)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Событие в истории"
        verbose_name_plural = "История компании"
        ordering = ['order', 'year']

    def __str__(self):
        return f"{self.year}: {self.title}"