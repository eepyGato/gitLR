# core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('branches/', views.branches, name='branches'),
    path('insurance-types/', views.insurance_types, name='insurance_types'),
    path('faq/', views.faq_list, name='faq'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('promo-codes/', views.promo_codes, name='promo_codes'),
    
    # Contract URLs - ПРАВИЛЬНЫЙ ПОРЯДОК
    path('contracts/create/', views.contract_create, name='contract_create'),  # сначала create
    path('contracts/<int:pk>/', views.contract_detail, name='contract_detail'),  # потом detail
    path('contracts/', views.contract_list, name='contract_list'),  # потом list
    path('contracts/<int:pk>/update/', views.contract_update, name='contract_update'),
    path('contracts/<int:pk>/delete/', views.contract_delete, name='contract_delete'),
    
    # Review URLs
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/create/', views.review_create, name='review_create'),
    path('reviews/<int:pk>/update/', views.review_update, name='review_update'),
    path('reviews/<int:pk>/delete/', views.review_delete, name='review_delete'),
    path('reviews/admin/create/', views.review_create_for_client, name='review_create_for_client'),
    path('reviews/admin/<int:pk>/edit/', views.review_admin_edit, name='review_admin_edit'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.client_profile_update, name='client_profile_update'),
    
    # Statistics and API
    path('statistics/', views.statistics, name='statistics'),
    path('api/exchange-rate/', views.api_exchange_rate, name='api_exchange_rate'),
    path('api/weather/', views.api_weather, name='api_weather'),

    # CRUD для новостей
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('news/create/', views.news_create, name='news_create'),
    path('news/<int:pk>/update/', views.news_update, name='news_update'),
    path('news/<int:pk>/delete/', views.news_delete, name='news_delete'),

    # История компании
    path('history/', views.history_list, name='history_list'),

    # Сотрудники
    path('staff/', views.staff_list, name='staff_list'),

    path('promo/apply/', views.apply_promo, name='apply_promo'),
]
