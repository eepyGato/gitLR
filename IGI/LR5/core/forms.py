# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from .models import (
    Client, InsuranceContract, Review, PromoCode,
    InsuranceAgent, Branch, InsuranceType, InsuredObject
)
import re
import logging
from .models import News, CompanyHistory, StaffMember

logger = logging.getLogger(__name__)


class PhoneNumberMixin:
    """Mixin for phone number validation"""
    
    def validate_phone(self, phone):
        pattern = r'^\+375\s\(\d{2}\)\s\d{3}-\d{2}-\d{2}$'
        if not re.match(pattern, phone):
            raise ValidationError(
                'Телефон должен быть в формате +375 (29) XXX-XX-XX'
            )
        return phone


class AgeValidationMixin:
    """Mixin for age validation (18+)"""
    
    def validate_age(self, birth_date):
        today = date.today()
        age = today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
        )
        if age < 18:
            raise ValidationError('Возраст должен быть 18 лет или больше')
        return birth_date


class UserRegistrationForm(UserCreationForm):
    """Form for user registration with client fields"""
    
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=100, required=True, label='Имя')
    last_name = forms.CharField(max_length=100, required=True, label='Фамилия')
    middle_name = forms.CharField(max_length=100, required=False, label='Отчество')
    address = forms.CharField(widget=forms.Textarea, required=True, label='Адрес')
    phone = forms.CharField(max_length=20, required=True, label='Телефон')
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True, label='Дата рождения')
    passport_number = forms.CharField(max_length=20, required=True, label='Номер паспорта')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        import re
        if not re.match(r'^\+375\s\(\d{2}\)\s\d{3}-\d{2}-\d{2}$', phone):
            raise ValidationError('Телефон должен быть в формате +375 (29) XXX-XX-XX')
        return phone
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        from datetime import date
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            raise ValidationError('Вам должно быть 18 лет или больше')
        return birth_date
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Создаём профиль клиента
            from .models import Client
            Client.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                middle_name=self.cleaned_data.get('middle_name', ''),
                address=self.cleaned_data['address'],
                phone=self.cleaned_data['phone'],
                email=self.cleaned_data['email'],
                birth_date=self.cleaned_data['birth_date'],
                passport_number=self.cleaned_data['passport_number']
            )
        return user


class ClientProfileForm(forms.ModelForm, PhoneNumberMixin, AgeValidationMixin):
    """Form for client profile"""
    
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'middle_name', 'address', 
                  'phone', 'email', 'birth_date', 'passport_number')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_phone(self):
        return self.validate_phone(self.cleaned_data.get('phone'))
    
    def clean_birth_date(self):
        return self.validate_age(self.cleaned_data.get('birth_date'))


class InsuranceContractForm(forms.ModelForm):
    """Form for insurance contract"""
    
    object_description = forms.CharField(
        max_length=200,
        required=True,
        label='Описание объекта страхования',
        widget=forms.TextInput(attrs={'placeholder': 'Например: Toyota Camry 2020, квартира, ...'})
    )
    object_value = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=True,
        label='Страховая стоимость объекта',
        help_text='Рыночная стоимость объекта (максимальная сумма выплаты)',
        widget=forms.NumberInput(attrs={'placeholder': 'Сумма в рублях', 'step': '0.01'})
    )
    promo_code = forms.CharField(
        max_length=50,
        required=False,
        label='🎫 Промокод',
        help_text='Введите промокод для получения скидки (если есть)',
        widget=forms.TextInput(attrs={'placeholder': 'Например: WELCOME10'})
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        from datetime import date, timedelta
    
        # Устанавливаем даты автоматически для всех
        self.fields['start_date'].initial = date.today()
        self.fields['end_date'].initial = date.today() + timedelta(days=365)
        
        # Скрываем поля с датами для всех пользователей (и админа, и клиента)
        self.fields['start_date'].widget = forms.HiddenInput()
        self.fields['end_date'].widget = forms.HiddenInput()
        
        # Делаем поля необязательными для ввода (они заполнятся автоматически)
        self.fields['start_date'].required = False
        self.fields['end_date'].required = False
        
        if user and not user.is_superuser:
            try:
                from .models import Client
                client = Client.objects.get(user=user)
                self.fields['client'].queryset = Client.objects.filter(id=client.id)
                self.fields['client'].initial = client
                self.fields['client'].widget = forms.HiddenInput()
            except Client.DoesNotExist:
                self.fields['client'].queryset = Client.objects.none()
                self.fields['client'].widget = forms.HiddenInput()
        
        # Ограничиваем агентов
        from .models import StaffMember
        self.fields['agent'].queryset = StaffMember.objects.filter(
            position='agent', 
            is_active=True
        )
        
        # Добавляем подсказки
        self.fields['insurance_sum'].help_text = 'Сумма, на которую вы страхуете объект (не может превышать страховую стоимость)'
        self.fields['insurance_sum'].widget.attrs.update({'step': '0.01', 'placeholder': 'Сумма в рублях'})
        self.fields['start_date'].help_text = 'Дата начала действия договора'
        self.fields['end_date'].help_text = 'Дата окончания действия договора'
        self.fields['agent'].help_text = 'Выберите страхового агента'
        self.fields['branch'].help_text = 'Выберите филиал'
        self.fields['insurance_type'].help_text = 'Выберите вид страхования (тариф будет применён автоматически)'
        
        # Скрываем tariff_rate
        self.fields['tariff_rate'].widget = forms.HiddenInput()
        self.fields['tariff_rate'].required = False
        
        # Скрываем insured_object
        self.fields['insured_object'].widget = forms.HiddenInput()
        self.fields['insured_object'].required = False
        
        # ===== ЭТА СТРОКА ОСТАЁТСЯ (или добавляем, если нет) =====
        if 'insurance_type' in self.fields:
            self.fields['insurance_type'].widget.attrs.update({'class': 'form-control'})
        
    class Meta:
        model = InsuranceContract
        fields = ('client', 'agent', 'branch', 'insurance_type', 
                'insured_object', 'insurance_sum', 'tariff_rate',
                'start_date', 'end_date')
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'insurance_sum': forms.NumberInput(attrs={'step': '0.01'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        insurance_sum = cleaned_data.get('insurance_sum')
        object_value = cleaned_data.get('object_value')
        insurance_type = cleaned_data.get('insurance_type')
        promo_code_value = cleaned_data.get('promo_code')
        
        # Проверка: страховая сумма не может превышать страховую стоимость
        if insurance_sum and object_value and insurance_sum > object_value:
            raise ValidationError('Страховая сумма не может превышать страховую стоимость объекта')
        
        # Проверка: страховая сумма должна быть положительной
        if insurance_sum and insurance_sum <= 0:
            raise ValidationError('Страховая сумма должна быть больше 0')
        
        # Проверка промокода
        if promo_code_value:
            from .models import PromoCode
            try:
                promo = PromoCode.objects.get(code=promo_code_value)
                if not promo.is_valid():
                    self.add_error('promo_code', 'Промокод недействителен или истёк')
                else:
                    cleaned_data['valid_promo'] = promo
            except PromoCode.DoesNotExist:
                self.add_error('promo_code', 'Промокод не найден')
        
        # Устанавливаем тарифную ставку из вида страхования
        if insurance_type:
            cleaned_data['tariff_rate'] = insurance_type.tariff_rate
        
        # Устанавливаем даты
        from datetime import date, timedelta
        if not cleaned_data.get('start_date'):
            cleaned_data['start_date'] = date.today()
        if not cleaned_data.get('end_date'):
            cleaned_data['end_date'] = date.today() + timedelta(days=365)
        
        return cleaned_data


    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Устанавливаем тарифную ставку из вида страхования
        if instance.insurance_type:
            instance.tariff_rate = instance.insurance_type.tariff_rate
        
        # Устанавливаем даты
        from datetime import date, timedelta
        if not instance.start_date:
            instance.start_date = date.today()
        if not instance.end_date:
            instance.end_date = date.today() + timedelta(days=365)
        
        # Создаём объект страхования
        object_type = 'property'
        if instance.insurance_type:
            type_name = instance.insurance_type.name.lower()
            if 'автомобил' in type_name or 'car' in type_name:
                object_type = 'car'
            elif 'медицин' in type_name or 'health' in type_name:
                object_type = 'health'
            elif 'жизн' in type_name or 'life' in type_name:
                object_type = 'life'
            elif 'путешеств' in type_name or 'travel' in type_name:
                object_type = 'travel'
        
        from .models import InsuredObject
        insured_object = InsuredObject.objects.create(
            client=instance.client,
            object_type=object_type,
            description=self.cleaned_data['object_description'],
            value=self.cleaned_data['object_value']
        )
        instance.insured_object = insured_object
        
        # Расчёт с учётом промокода
        insurance_payment = instance.insurance_sum * instance.tariff_rate / 100
        instance.insurance_payment = insurance_payment
        
        promo = self.cleaned_data.get('valid_promo')
        if promo:
            discount = insurance_payment * promo.discount_percent / 100
            instance.final_payment = insurance_payment - discount
            # Увеличиваем счётчик использования промокода
            promo.used_count += 1
            promo.save()
        else:
            instance.final_payment = insurance_payment
        
        if commit:
            instance.save()
        return instance
        

        


class ReviewForm(forms.ModelForm):
    """Form for client review"""
    
    class Meta:
        model = Review
        fields = ('rating', 'text')
        widgets = {
            'rating': forms.Select(choices=[(i, f"{i} звезд") for i in range(1, 6)]),
            'text': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Ваш отзыв...'}),
        }
    
    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) < 10:
            raise ValidationError('Текст отзыва должен содержать не менее 10 символов')
        return text


class PromoCodeApplyForm(forms.Form):
    """Form for applying promo code"""
    
    promo_code = forms.CharField(max_length=50, label='Промокод')
    
    def clean_promo_code(self):
        code = self.cleaned_data.get('promo_code')
        try:
            promo = PromoCode.objects.get(code=code)
            if not promo.is_valid():
                raise ValidationError('Промокод недействителен или истёк')
            return promo
        except PromoCode.DoesNotExist:
            raise ValidationError('Промокод не найден')


class InsuranceAgentForm(forms.ModelForm, PhoneNumberMixin, AgeValidationMixin):
    """Form for insurance agent"""
    
    class Meta:
        model = InsuranceAgent
        fields = ('first_name', 'last_name', 'middle_name', 'address',
                  'phone', 'birth_date', 'branch', 'hire_date')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_phone(self):
        return self.validate_phone(self.cleaned_data.get('phone'))
    
    def clean_birth_date(self):
        return self.validate_age(self.cleaned_data.get('birth_date'))


class SearchForm(forms.Form):
    """Form for searching contracts"""
    
    query = forms.CharField(
        max_length=100, 
        required=False,
        label='Поиск',
        widget=forms.TextInput(attrs={'placeholder': 'Номер договора, ФИО клиента...'})
    )
    insurance_type = forms.ModelChoiceField(
        queryset=InsuranceType.objects.filter(is_active=True),
        required=False,
        label='Вид страхования'
    )
    branch = forms.ModelChoiceField(
        queryset=Branch.objects.all(),
        required=False,
        label='Филиал'
    )
    status = forms.ChoiceField(
        choices=[('', 'Все')] + list(InsuranceContract.STATUS_CHOICES),
        required=False,
        label='Статус'
    )
    date_from = forms.DateField(
        required=False,
        label='Дата от',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    date_to = forms.DateField(
        required=False,
        label='Дата до',
        widget=forms.DateInput(attrs={'type': 'date'})
    )


class DateRangeForm(forms.Form):
    """Form for date range selection for statistics"""
    
    date_from = forms.DateField(
        required=False,
        label='Дата от',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    date_to = forms.DateField(
        required=False,
        label='Дата до',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

class NewsForm(forms.ModelForm):
    """Форма для новостей"""
    
    class Meta:
        model = News
        fields = ['title', 'short_description', 'content', 'image', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
            'short_description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise ValidationError('Заголовок должен содержать минимум 5 символов')
        return title


class CompanyHistoryForm(forms.ModelForm):
    """Форма для истории компании"""
    
    class Meta:
        model = CompanyHistory
        fields = ['year', 'title', 'description', 'image', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class StaffMemberForm(forms.ModelForm):
    """Форма для сотрудников"""
    
    class Meta:
        model = StaffMember
        fields = ['full_name', 'position', 'department', 'phone', 'email', 
                  'photo', 'bio', 'hire_date', 'is_active', 'order']
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 5}),
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Валидация телефона
        import re
        if not re.match(r'^\+375\s\(\d{2}\)\s\d{3}-\d{2}-\d{2}$', phone):
            raise ValidationError('Телефон должен быть в формате +375 (29) XXX-XX-XX')
        return phone