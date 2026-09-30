# add_test_data.py
import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insurance_firm.settings')
django.setup()

from core.models import (
    Branch, InsuranceType, InsuranceAgent, Client, 
    InsuranceContract, News, FAQ, Vacancy, Review, 
    PromoCode, StaffMember
)

def add_test_data():
    print("=" * 60)
    print("Добавление тестовых данных...")
    print("=" * 60)
    
    # 1. Филиалы
    if Branch.objects.count() == 0:
        branches = [
            Branch(name="Центральный офис", address="г. Минск, ул. Ленина, 1", phone="+375 (29) 111-11-11"),
            Branch(name="Филиал на Немиге", address="г. Минск, ул. Немига, 10", phone="+375 (29) 222-22-22"),
            Branch(name="Филиал в Гродно", address="г. Гродно, ул. Советская, 15", phone="+375 (29) 333-33-33"),
            Branch(name="Филиал в Бресте", address="г. Брест, ул. Московская, 20", phone="+375 (29) 444-44-44"),
        ]
        Branch.objects.bulk_create(branches)
        print(f"✅ Добавлено филиалов: {Branch.objects.count()}")
    
    # 2. Виды страхования
    if InsuranceType.objects.count() == 0:
        types = [
            InsuranceType(name="Страхование автомобиля", commission_percent=10.00),
            InsuranceType(name="Страхование имущества", commission_percent=12.00),
            InsuranceType(name="Медицинское страхование", commission_percent=8.00),
            InsuranceType(name="Страхование жизни", commission_percent=15.00),
        ]
        InsuranceType.objects.bulk_create(types)
        print(f"✅ Добавлено видов страхования: {InsuranceType.objects.count()}")
    
    # 3. Новости
    if News.objects.count() == 0:
        news = [
            News(title="Новая программа страхования", 
                 short_description="Запущена новая программа страхования жизни",
                 content="Мы рады сообщить о запуске новой программы...",
                 is_published=True),
            News(title="Скидки для новых клиентов", 
                 short_description="Специальное предложение для новых клиентов",
                 content="При оформлении страховки до конца месяца скидка 15%...",
                 is_published=True),
        ]
        News.objects.bulk_create(news)
        print(f"✅ Добавлено новостей: {News.objects.count()}")
    
    # 4. FAQ
    if FAQ.objects.count() == 0:
        faqs = [
            FAQ(question="Как оформить страховку?", 
                answer="Обратитесь в любой наш филиал с паспортом", 
                is_published=True),
            FAQ(question="Какие документы нужны?", 
                answer="Паспорт и документы на объект страхования", 
                is_published=True),
            FAQ(question="Как получить выплату?", 
                answer="Подайте заявление в филиале с документами", 
                is_published=True),
        ]
        FAQ.objects.bulk_create(faqs)
        print(f"✅ Добавлено вопросов: {FAQ.objects.count()}")
    
    # 5. Вакансии
    if Vacancy.objects.count() == 0:
        vacancies = [
            Vacancy(title="Страховой агент", 
                    description="Привлекаем клиентов, заключаем договоры",
                    requirements="Опыт от 1 года", 
                    salary_from=1000, salary_to=3000,
                    location="Минск", is_active=True),
            Vacancy(title="Менеджер по продажам", 
                    description="Управление отделом продаж",
                    requirements="Опыт управления от 3 лет", 
                    salary_from=2000, salary_to=5000,
                    location="Минск", is_active=True),
        ]
        Vacancy.objects.bulk_create(vacancies)
        print(f"✅ Добавлено вакансий: {Vacancy.objects.count()}")
    
    # 6. Промокоды
    if PromoCode.objects.count() == 0:
        from django.utils import timezone
        promos = [
            PromoCode(code="WELCOME10", discount_percent=10.00,
                     valid_from=timezone.now(), 
                     valid_to=timezone.now() + timedelta(days=30),
                     is_active=True),
            PromoCode(code="SUMMER20", discount_percent=20.00,
                     valid_from=timezone.now(), 
                     valid_to=timezone.now() + timedelta(days=60),
                     is_active=True),
        ]
        PromoCode.objects.bulk_create(promos)
        print(f"✅ Добавлено промокодов: {PromoCode.objects.count()}")
    
    print("\n" + "=" * 60)
    print("📊 Итог:")
    print(f"  - Филиалы: {Branch.objects.count()}")
    print(f"  - Виды страхования: {InsuranceType.objects.count()}")
    print(f"  - Новости: {News.objects.count()}")
    print(f"  - FAQ: {FAQ.objects.count()}")
    print(f"  - Вакансии: {Vacancy.objects.count()}")
    print(f"  - Промокоды: {PromoCode.objects.count()}")
    print("=" * 60)

if __name__ == "__main__":
    add_test_data()