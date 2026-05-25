# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Sum, Count, Avg, Min, Max
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import datetime, timedelta, date
from statistics import mean, median, mode
import requests
import logging
from .models import News, CompanyHistory, StaffMember
from .forms import NewsForm, CompanyHistoryForm, StaffMemberForm
from django.urls import reverse



from .models import (
    Branch, InsuranceType, InsuranceAgent, Client, InsuredObject,
    InsuranceContract, PromoCode, Review, FAQ, Vacancy, CompanyInfo, Contact
)
from .forms import (
    UserRegistrationForm, ClientProfileForm, InsuranceContractForm,
    ReviewForm, PromoCodeApplyForm, SearchForm, DateRangeForm
)

logger = logging.getLogger(__name__)


# ========== Helper functions ==========

def is_admin(user):
    """Check if user is superuser"""
    return user.is_superuser


def is_agent(user):
    """Check if user is insurance agent"""
    if not user.is_authenticated:
        return False
    return InsuranceAgent.objects.filter(user=user, is_active=True).exists()


def is_client(user):
    """Check if user is client"""
    if not user.is_authenticated:
        return False
    return Client.objects.filter(user=user).exists()


def get_client_from_user(user):
    """Get client profile from user"""
    try:
        return Client.objects.get(user=user)
    except Client.DoesNotExist:
        return None


def get_agent_from_user(user):
    """Get agent profile from user"""
    try:
        return InsuranceAgent.objects.get(user=user, is_active=True)
    except InsuranceAgent.DoesNotExist:
        return None


# ========== Main pages ==========

def home(request):
    """Home page - show latest articles/news"""
    logger.info(f"Home page accessed by {request.user if request.user.is_authenticated else 'Anonymous'}")
    
    # Latest reviews
    latest_reviews = Review.objects.filter(is_published=True)[:5]
    
    # Latest vacancies
    latest_vacancies = Vacancy.objects.filter(is_active=True)[:3]
    
    # Latest FAQs
    latest_faqs = FAQ.objects.filter(is_published=True)[:5]
    
    # Statistics for home page
    total_clients = Client.objects.count()
    total_contracts = InsuranceContract.objects.filter(status='active').count()
    total_branches = Branch.objects.count()
    
    # Get current time in user's timezone
    current_time = timezone.now()
    
    context = {
        'latest_reviews': latest_reviews,
        'latest_vacancies': latest_vacancies,
        'latest_faqs': latest_faqs,
        'total_clients': total_clients,
        'total_contracts': total_contracts,
        'total_branches': total_branches,
        'current_time': current_time,
    }
    return render(request, 'core/home.html', context)


def about(request):
    """About company page"""
    try:
        company_info = CompanyInfo.objects.first()
    except CompanyInfo.DoesNotExist:
        company_info = None

    staff_members = StaffMember.objects.filter(is_active=True).order_by('order', 'full_name')

    contacts = Contact.objects.all()

    #for debug reasons only))
    print(f"Найдено сотрудников: {staff_members.count()}")
    for s in staff_members:
        print(f"  - {s.full_name}")
    
    context = {
        'company_info': company_info,
        'contacts': contacts,
        'staff_members': staff_members,
    }
    return render(request, 'core/about.html', context)


def branches(request):
    """Branches list page"""
    branches_list = Branch.objects.all()
    
    # Calculate statistics for each branch
    for branch in branches_list:
        branch.contracts_count = InsuranceContract.objects.filter(branch=branch).count()
        branch.total_insurance_sum = InsuranceContract.objects.filter(
            branch=branch, status='active'
        ).aggregate(Sum('insurance_sum'))['insurance_sum__sum'] or 0
    
    context = {'branches': branches_list}
    return render(request, 'core/branches.html', context)


def insurance_types(request):
    """Insurance types list page"""
    types = InsuranceType.objects.filter(is_active=True)
    
    for ins_type in types:
        ins_type.contracts_count = InsuranceContract.objects.filter(
            insurance_type=ins_type, status='active'
        ).count()
    
    context = {'insurance_types': types}
    return render(request, 'core/insurance_types.html', context)


def faq_list(request):
    """FAQ list page"""
    faqs = FAQ.objects.filter(is_published=True)
    context = {'faqs': faqs}
    return render(request, 'core/faq.html', context)


def vacancies(request):
    """Vacancies list page"""
    vacancies_list = Vacancy.objects.filter(is_active=True)
    context = {'vacancies': vacancies_list}
    return render(request, 'core/vacancies.html', context)


def privacy_policy(request):
    """Privacy policy page"""
    return render(request, 'core/privacy_policy.html')


def promo_codes(request):
    """Promo codes list page"""
    active_promos = PromoCode.objects.filter(is_active=True)
    expired_promos = PromoCode.objects.filter(is_active=False)
    
    context = {
        'active_promos': active_promos,
        'expired_promos': expired_promos,
    }
    return render(request, 'core/promo_codes.html', context)

def apply_promo(request):
    """Apply promo code"""
    if request.method == 'POST':
        form = PromoCodeApplyForm(request.POST)
        if form.is_valid():
            promo = form.cleaned_data['promo_code']
            
            # Увеличиваем счётчик использования
            promo.used_count += 1
            promo.save()
            
            # Сохраняем промокод в сессии
            request.session['active_promo'] = {
                'code': promo.code,
                'discount_percent': float(promo.discount_percent)
            }
            
            messages.success(request, f'Промокод {promo.code} активирован! Скидка {promo.discount_percent}%')
        else:
            messages.error(request, 'Неверный или недействительный промокод')
    
    return redirect('core:promo_codes')


# ========== Contract views ==========

def contract_list(request):
    """List of contracts with filtering and search"""
    
    # Проверка авторизации
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Базовый запрос в зависимости от прав пользователя
    if request.user.is_superuser:
        # Админ видит все договоры
        contracts = InsuranceContract.objects.select_related(
            'client', 'agent', 'branch', 'insurance_type'
        )
    else:
        # Обычный пользователь видит ТОЛЬКО свои договоры
        try:
            client = Client.objects.get(user=request.user)
            contracts = InsuranceContract.objects.filter(client=client).select_related(
                'client', 'agent', 'branch', 'insurance_type'
            )
        except Client.DoesNotExist:
            # Если пользователь не является клиентом, показываем пустой список
            contracts = InsuranceContract.objects.none()
            messages.warning(request, 'Вы не зарегистрированы как клиент. Обратитесь в офис.')
    
    # Поиск и фильтрация
    search_form = SearchForm(request.GET)
    
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        if query:
            contracts = contracts.filter(
                Q(contract_number__icontains=query) |
                Q(client__last_name__icontains=query) |
                Q(client__first_name__icontains=query)
            )
        
        insurance_type = search_form.cleaned_data.get('insurance_type')
        if insurance_type:
            contracts = contracts.filter(insurance_type=insurance_type)
        
        branch = search_form.cleaned_data.get('branch')
        if branch:
            contracts = contracts.filter(branch=branch)
        
        status = search_form.cleaned_data.get('status')
        if status:
            contracts = contracts.filter(status=status)
        
        date_from = search_form.cleaned_data.get('date_from')
        if date_from:
            contracts = contracts.filter(start_date__gte=date_from)
        
        date_to = search_form.cleaned_data.get('date_to')
        if date_to:
            contracts = contracts.filter(end_date__lte=date_to)
    
    # Сортировка
    sort_by = request.GET.get('sort', '-created_at')
    allowed_sorts = ['contract_number', 'insurance_sum', 'start_date', 'created_at', 
                     '-contract_number', '-insurance_sum', '-start_date', '-created_at']
    if sort_by in allowed_sorts:
        contracts = contracts.order_by(sort_by)
    
    # Пагинация
    paginator = Paginator(contracts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'contracts': page_obj,
        'search_form': search_form,
        'sort_by': sort_by,
    }
    return render(request, 'core/contract_list.html', context)

@login_required
def contract_detail(request, pk):
    """Contract detail page"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    contract = get_object_or_404(InsuranceContract, pk=pk)
    
    # Проверка доступа
    if not request.user.is_superuser:
        try:
            client = Client.objects.get(user=request.user)
            if contract.client != client:
                messages.error(request, 'У вас нет доступа к этому договору')
                return redirect('contract_list')
        except Client.DoesNotExist:
            messages.error(request, 'Доступ запрещён')
            return redirect('contract_list')
    
    insurance_payment = contract.insurance_payment()
    agent_commission = contract.agent_commission()
    
    context = {
        'contract': contract,
        'insurance_payment': insurance_payment,
        'agent_commission': agent_commission,
    }
    return render(request, 'core/contract_detail.html', context)


@login_required
def contract_create(request):
    # Проверяем, есть ли активированный промокод в сессии
    active_promo = request.session.get('active_promo')
    
    if request.method == 'POST':
        form = InsuranceContractForm(request.POST, user=request.user)
        if form.is_valid():
            contract = form.save()
            
            # Очищаем промокод из сессии после использования
            if 'active_promo' in request.session:
                del request.session['active_promo']
            
            return redirect('core:contract_detail', pk=contract.pk)
    else:
        form = InsuranceContractForm(user=request.user)
        if active_promo:
            form.fields['promo_code'].initial = active_promo['code']
    
    return render(request, 'core/contract_form.html', {'form': form})

@login_required
def contract_update(request, pk):
    """Update insurance contract"""
    contract = get_object_or_404(InsuranceContract, pk=pk)
    
    if request.method == 'POST':
        form = InsuranceContractForm(request.POST, instance=contract)
        if form.is_valid():
            form.save()
            messages.success(request, f'Договор {contract.contract_number} успешно обновлён!')
            logger.info(f"User {request.user} updated contract {contract.contract_number}")
            return redirect('core:contract_detail', pk=contract.pk)
    else:
        form = InsuranceContractForm(instance=contract)
    
    context = {'form': form, 'contract': contract}
    return render(request, 'core/contract_form.html', context)


@login_required
@user_passes_test(is_admin)
def contract_delete(request, pk):
    """Delete insurance contract (admin only)"""
    contract = get_object_or_404(InsuranceContract, pk=pk)
    contract_number = contract.contract_number
    
    if request.method == 'POST':
        contract.delete()
        messages.success(request, f'Договор {contract_number} удалён')
        logger.warning(f"User {request.user} deleted contract {contract_number}")
        return redirect('contract_list')
    
    context = {'contract': contract}
    return render(request, 'core/contract_confirm_delete.html', context)


# ========== Review views ==========

def review_list(request):
    """List of reviews"""
    reviews = Review.objects.filter(is_published=True)
    
    # Statistics
    if reviews.exists():
        ratings = [r.rating for r in reviews]
        avg_rating = mean(ratings)
        median_rating = median(ratings)
        try:
            mode_rating = mode(ratings)
        except:
            mode_rating = None
    else:
        avg_rating = median_rating = mode_rating = None
    
    context = {
        'reviews': reviews,
        'avg_rating': avg_rating,
        'median_rating': median_rating,
        'mode_rating': mode_rating,
    }
    return render(request, 'core/review_list.html', context)


@login_required
def review_create(request):
    """Create new review (only one per client)"""
    if not request.user.is_authenticated:
        messages.error(request, 'Пожалуйста, войдите в систему чтобы оставить отзыв')
        return redirect('login')
    
    # Для админа - показываем форму выбора клиента
    if request.user.is_superuser:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                client_id = request.POST.get('client_id')
                if client_id:
                    try:
                        review.client = Client.objects.get(id=client_id)
                        review.save()
                        messages.success(request, 'Отзыв успешно создан!')
                        return redirect('core:review_list')
                    except Client.DoesNotExist:
                        messages.error(request, 'Клиент не найден')
                else:
                    messages.error(request, 'Выберите клиента')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{error}')
        else:
            form = ReviewForm()
        
        # Получаем список клиентов для выбора
        clients = Client.objects.all()
        
        context = {
            'form': form,
            'clients': clients,
            'is_admin': True,
            'is_edit': False,
        }
        return render(request, 'core/review_form.html', context)
    
    # Для обычного пользователя (как было раньше)
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        messages.error(request, 'Только клиенты могут оставлять отзывы')
        return redirect('core:home')
    
    existing_review = Review.objects.filter(client=client).first()
    
    if existing_review:
        return redirect('core:review_update', pk=existing_review.pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.client = client
            review.save()
            messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('core:review_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'client': client,
        'is_admin': False,
        'is_edit': False,
    }
    return render(request, 'core/review_form.html', context)


def review_update(request, pk):
    """Edit existing review"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    review = get_object_or_404(Review, pk=pk)
    
    # Проверка прав
    if not request.user.is_superuser:
        try:
            client = Client.objects.get(user=request.user)
            if review.client != client:
                messages.error(request, 'Вы можете редактировать только свои отзывы')
                return redirect('core:review_list')
        except Client.DoesNotExist:
            messages.error(request, 'Доступ запрещён')
            return redirect('core:review_list')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Отзыв успешно обновлён!')
            return redirect('core:review_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = ReviewForm(instance=review)
    
    context = {
        'form': form,
        'review': review,
        'is_edit': True,
    }
    return render(request, 'core/review_form.html', context)


def review_delete(request, pk):
    """Delete review (admin only)"""
    if not request.user.is_superuser:
        messages.error(request, 'У вас нет прав для удаления отзывов')
        return redirect('core:review_list')
    
    review = get_object_or_404(Review, pk=pk)
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Отзыв удалён')
        return redirect('core:review_list')
    
    return render(request, 'core/review_confirm_delete.html', {'review': review})

# ========== User authentication views ==========

def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            logger.info(f"New user registered: {user.username}")
            messages.success(request, 'Регистрация успешна! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    context = {'form': form}
    return render(request, 'core/register.html', context)


@login_required
def profile(request):
    """User profile page"""
    user = request.user
    client = get_client_from_user(user)
    agent = get_agent_from_user(user)
    
    context = {
        'user': user,
        'client': client,
        'agent': agent,
    }
    return render(request, 'core/profile.html', context)


@login_required
def client_profile_update(request):
    """Update client profile"""
    client = get_client_from_user(request.user)
    
    if not client:
        messages.error(request, 'Профиль клиента не найден')
        return redirect('profile')
    
    if request.method == 'POST':
        form = ClientProfileForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлён!')
            return redirect('profile')
    else:
        form = ClientProfileForm(instance=client)
    
    context = {'form': form}
    return render(request, 'core/client_profile_form.html', context)


# ========== Statistics and API views ==========

def statistics(request):
    """Statistics page with charts"""
    # Get date range
    form = DateRangeForm(request.GET)
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    contracts = InsuranceContract.objects.all()
    
    if date_from:
        contracts = contracts.filter(start_date__gte=date_from)
    if date_to:
        contracts = contracts.filter(start_date__lte=date_to)
    
    # Basic statistics
    total_contracts = contracts.count()
    total_clients = Client.objects.count()
    total_agents = InsuranceAgent.objects.filter(is_active=True).count()
    total_branches = Branch.objects.count()
    
    # Financial statistics
    total_insurance_sum = contracts.aggregate(Sum('insurance_sum'))['insurance_sum__sum'] or 0
    total_insurance_payment = sum(c.insurance_payment() for c in contracts)
    total_agent_commission = sum(c.agent_commission() for c in contracts)
    
    # Statistics by insurance type
    type_stats = []
    for ins_type in InsuranceType.objects.filter(is_active=True):
        type_contracts = contracts.filter(insurance_type=ins_type)
        if type_contracts.exists():
            type_stats.append({
                'name': ins_type.name,
                'count': type_contracts.count(),
                'total_sum': type_contracts.aggregate(Sum('insurance_sum'))['insurance_sum__sum'] or 0,
            })
    
    # Statistics by branch
    branch_stats = []
    for branch in Branch.objects.all():
        branch_contracts = contracts.filter(branch=branch)
        if branch_contracts.exists():
            branch_stats.append({
                'name': branch.name,
                'count': branch_contracts.count(),
                'total_sum': branch_contracts.aggregate(Sum('insurance_sum'))['insurance_sum__sum'] or 0,
            })
    
    # Monthly statistics
    monthly_stats = {}
    for contract in contracts:
        month = contract.start_date.strftime('%Y-%m')
        if month not in monthly_stats:
            monthly_stats[month] = {'count': 0, 'sum': 0}
        monthly_stats[month]['count'] += 1
        monthly_stats[month]['sum'] += float(contract.insurance_sum)
    
    # Statistical measures for insurance sums
    insurance_sums = [float(c.insurance_sum) for c in contracts]
    if insurance_sums:
        mean_sum = mean(insurance_sums)
        median_sum = median(insurance_sums)
        try:
            mode_sum = mode(insurance_sums)
        except:
            mode_sum = None
        min_sum = min(insurance_sums)
        max_sum = max(insurance_sums)
    else:
        mean_sum = median_sum = mode_sum = min_sum = max_sum = None
    
    # Most popular insurance type
    most_popular_type = max(type_stats, key=lambda x: x['count']) if type_stats else None
    
    # Most profitable insurance type
    most_profitable_type = max(type_stats, key=lambda x: x['total_sum']) if type_stats else None
    
    context = {
        'form': form,
        'total_contracts': total_contracts,
        'total_clients': total_clients,
        'total_agents': total_agents,
        'total_branches': total_branches,
        'total_insurance_sum': total_insurance_sum,
        'total_insurance_payment': total_insurance_payment,
        'total_agent_commission': total_agent_commission,
        'type_stats': type_stats,
        'branch_stats': branch_stats,
        'monthly_stats': dict(sorted(monthly_stats.items())),
        'mean_sum': round(mean_sum, 2) if mean_sum else None,
        'median_sum': round(median_sum, 2) if median_sum else None,
        'mode_sum': round(mode_sum, 2) if mode_sum else None,
        'min_sum': min_sum,
        'max_sum': max_sum,
        'most_popular_type': most_popular_type,
        'most_profitable_type': most_profitable_type,
    }
    
    return render(request, 'core/statistics.html', context)


def api_exchange_rate(request):
    """API endpoint for currency exchange rates"""
    try:
        # Using free API for exchange rates (example)
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        data = response.json()
        
        rates = {
            'USD': data.get('rates', {}).get('USD', 1),
            'EUR': data.get('rates', {}).get('EUR', 0.85),
            'RUB': data.get('rates', {}).get('RUB', 90),
            'BYN': data.get('rates', {}).get('BYN', 3.2),
        }
        
        logger.info("Exchange rates fetched successfully")
        return JsonResponse({'success': True, 'rates': rates})
    except Exception as e:
        logger.error(f"Error fetching exchange rates: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


def api_weather(request):
    """API endpoint for weather (example)"""
    try:
        # Using free API for weather (example)
        response = requests.get('https://wttr.in/Minsk?format=j1')
        data = response.json()
        
        weather = {
            'temp': data.get('current_condition', [{}])[0].get('temp_C', 'N/A'),
            'humidity': data.get('current_condition', [{}])[0].get('humidity', 'N/A'),
            'wind': data.get('current_condition', [{}])[0].get('windspeedKmph', 'N/A'),
            'description': data.get('current_condition', [{}])[0].get('weatherDesc', [{}])[0].get('value', 'N/A'),
        }
        
        logger.info("Weather data fetched successfully")
        return JsonResponse({'success': True, 'weather': weather})
    except Exception as e:
        logger.error(f"Error fetching weather: {e}")
        return JsonResponse({'success': False, 'error': str(e)})

# ========== CRUD для новостей ==========

def news_list(request):
    """Список новостей"""
    news_list = News.objects.filter(is_published=True)
    
    # Поиск
    query = request.GET.get('q', '')
    if query:
        news_list = news_list.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    
    # Сортировка
    sort = request.GET.get('sort', '-created_at')
    if sort in ['title', 'created_at', '-title', '-created_at']:
        news_list = news_list.order_by(sort)
    
    return render(request, 'core/news_list.html', {'news_list': news_list, 'query': query})


def news_detail(request, pk):
    """Детальная страница новости"""
    news = get_object_or_404(News, pk=pk, is_published=True)
    return render(request, 'core/news_detail.html', {'news': news})


@login_required
@user_passes_test(is_admin)
def news_create(request):
    """Создание новости"""
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save()
            messages.success(request, f'Новость "{news.title}" создана!')
            return redirect('core:news_detail', pk=news.pk)
    else:
        form = NewsForm()
    return render(request, 'core/news_form.html', {'form': form, 'title': 'Создание новости'})


@login_required
@user_passes_test(is_admin)
def news_update(request, pk):
    """Обновление новости"""
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, f'Новость "{news.title}" обновлена!')
            return redirect('core:news_detail', pk=news.pk)
    else:
        form = NewsForm(instance=news)
    return render(request, 'core/news_form.html', {'form': form, 'title': 'Редактирование новости', 'news': news})


@login_required
@user_passes_test(is_admin)
def news_delete(request, pk):
    """Удаление новости"""
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        title = news.title
        news.delete()
        messages.success(request, f'Новость "{title}" удалена!')
        return redirect('core:news_list')
    return render(request, 'core/news_confirm_delete.html', {'news': news})


# ========== История компании ==========

def history_list(request):
    """Список истории компании"""
    history_items = CompanyHistory.objects.all().order_by('order', 'year')
    return render(request, 'core/history_list.html', {'history_items': history_items})


# ========== Сотрудники ==========

def staff_list(request):
    """Список сотрудников"""
    staff_members = StaffMember.objects.filter(is_active=True).order_by('order', 'full_name')
    return render(request, 'core/staff_list.html', {'staff_members': staff_members})