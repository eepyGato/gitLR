# core/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Branch, InsuranceType, InsuranceAgent, Client, InsuredObject,
    InsuranceContract, PromoCode, Review, FAQ, StaffMember, Vacancy, CompanyInfo, Contact,
    News, CompanyHistory
)
import logging

logger = logging.getLogger(__name__)


class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created_at')
    search_fields = ('name', 'address')
    list_filter = ('created_at',)


class InsuranceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'commission_percent', 'tariff_rate', 'is_active', 'created_at')  # Добавлен tariff_rate
    search_fields = ('name',)
    list_filter = ('is_active', 'created_at')
    list_editable = ('commission_percent', 'tariff_rate', 'is_active')  # Добавлен tariff_rate для редактирования


class InsuranceAgentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'branch', 'phone', 'age_display', 'is_active')
    search_fields = ('last_name', 'first_name', 'phone')
    list_filter = ('branch', 'is_active', 'hire_date')
    list_editable = ('is_active',)
    fieldsets = (
        ('Личная информация', {
            'fields': ('first_name', 'last_name', 'middle_name', 'birth_date')
        }),
        ('Контактная информация', {
            'fields': ('address', 'phone')
        }),
        ('Рабочая информация', {
            'fields': ('branch', 'hire_date', 'is_active', 'user')
        }),
    )
    
    def age_display(self, obj):
        return f"{obj.age()} лет"
    age_display.short_description = 'Возраст'
    
    def save_model(self, request, obj, form, change):
        logger.info(f"Администратор {request.user} изменил агента {obj}")
        super().save_model(request, obj, form, change)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'phone', 'email', 'age_display', 'created_at')
    search_fields = ('last_name', 'first_name', 'phone', 'email', 'passport_number')
    list_filter = ('created_at',)
    
    def age_display(self, obj):
        return f"{obj.age()} лет"
    age_display.short_description = 'Возраст'


class InsuredObjectAdmin(admin.ModelAdmin):
    list_display = ('client', 'object_type', 'value', 'created_at')
    search_fields = ('client__last_name', 'description')
    list_filter = ('object_type', 'created_at')


class InsuranceContractAdmin(admin.ModelAdmin):
    list_display = ('contract_number', 'client', 'insurance_type', 'insurance_sum', 
                   'status', 'insurance_payment_display', 'agent_commission_display')
    search_fields = ('contract_number', 'client__last_name', 'client__first_name')
    list_filter = ('status', 'insurance_type', 'branch', 'start_date', 'end_date')
    readonly_fields = ('contract_number', 'created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('contract_number', 'client', 'agent', 'branch', 'insurance_type')
        }),
        ('Объект страхования', {
            'fields': ('insured_object',)
        }),
        ('Финансовая информация', {
            'fields': ('insurance_sum', 'tariff_rate')
        }),
        ('Даты и статус', {
            'fields': ('start_date', 'end_date', 'status')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def insurance_payment_display(self, obj):
        return f"{obj.insurance_payment():,.2f}"
    insurance_payment_display.short_description = 'Страховой платёж'
    
    def agent_commission_display(self, obj):
        return f"{obj.agent_commission():,.2f}"
    agent_commission_display.short_description = 'Комиссия агента'


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'valid_from', 'valid_to', 
                   'is_active', 'used_count', 'max_uses')
    search_fields = ('code',)
    list_filter = ('is_active', 'valid_from', 'valid_to')
    list_editable = ('is_active', 'discount_percent')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client', 'rating', 'is_published', 'created_at')
    search_fields = ('client__last_name', 'text')
    list_filter = ('rating', 'is_published', 'created_at')
    list_editable = ('is_published',)


class FAQAdmin(admin.ModelAdmin):
    list_display = ('question_preview', 'is_published', 'created_at')
    search_fields = ('question', 'answer')
    list_filter = ('is_published', 'created_at')
    list_editable = ('is_published',)
    
    def question_preview(self, obj):
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    question_preview.short_description = 'Вопрос'


class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('is_active', 'location', 'created_at')
    list_editable = ('is_active',)


class CompanyInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not CompanyInfo.objects.exists()
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'short_description', 'full_description', 'logo', 'video_url')
        }),
        ('Юридическая информация', {
            'fields': ('foundation_year', 'ceo_name', 'employees_count', 
                      'legal_address', 'actual_address', 'inn', 'kpp', 'ogrn')
        }),
        ('Банковские реквизиты', {
            'fields': ('bank_name', 'bank_account', 'bik')
        }),
    )


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1


class CompanyInfoWithContactsAdmin(CompanyInfoAdmin):
    inlines = [ContactInline]


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)


class CompanyHistoryAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'description')


# Register all models
admin.site.register(Branch, BranchAdmin)
admin.site.register(InsuranceType, InsuranceTypeAdmin)
# admin.site.register(InsuranceAgent, InsuranceAgentAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(InsuredObject, InsuredObjectAdmin)
admin.site.register(InsuranceContract, InsuranceContractAdmin)
admin.site.register(PromoCode, PromoCodeAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(CompanyInfo, CompanyInfoWithContactsAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(CompanyHistory, CompanyHistoryAdmin)

class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'department', 'phone', 'email', 'is_active', 'order')
    list_filter = ('position', 'department', 'is_active', 'hire_date')
    search_fields = ('full_name', 'email', 'phone')
    list_editable = ('is_active', 'order')
    list_per_page = 20
    fieldsets = (
        ('Личная информация', {
            'fields': ('full_name', 'position', 'department')
        }),
        ('Контактная информация', {
            'fields': ('phone', 'email')
        }),
        ('Рабочая информация', {
            'fields': ('hire_date', 'is_active', 'order', 'bio')
        }),
        ('Фото', {
            'fields': ('photo',),
            'classes': ('collapse',)
        }),
    )
    
    def age_display(self, obj):
        return f"{obj.age()} лет"
    age_display.short_description = 'Возраст'

# Зарегистрируйте модель
admin.site.register(StaffMember, StaffMemberAdmin)