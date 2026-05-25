# generate_test_data.py
import os
import django
import random
from datetime import date, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insurance_firm.settings')
django.setup()

from core.models import (
    Branch, InsuranceType, StaffMember, Client, 
    InsuredObject, InsuranceContract
)

def generate_test_data():
    print("=" * 60)
    print("ГЕНЕРАЦИЯ ТЕСТОВЫХ ДАННЫХ ДЛЯ СТАТИСТИКИ")
    print("=" * 60)
    
    # ========== 1. ФИЛИАЛЫ ==========
    print("\n1. Проверка филиалов...")
    branches = [
        {"name": "Центральный офис", "address": "г. Минск, ул. Ленина, 1", "phone": "+375 (29) 111-11-11"},
        {"name": "Филиал на Немиге", "address": "г. Минск, ул. Немига, 10", "phone": "+375 (29) 222-22-22"},
        {"name": "Филиал на Победителей", "address": "г. Минск, пр. Победителей, 100", "phone": "+375 (29) 333-33-33"},
        {"name": "Филиал в Гродно", "address": "г. Гродно, ул. Советская, 15", "phone": "+375 (29) 444-44-44"},
        {"name": "Филиал в Бресте", "address": "г. Брест, ул. Московская, 20", "phone": "+375 (29) 555-55-55"},
    ]
    
    branch_objects = []
    for b in branches:
        obj, created = Branch.objects.get_or_create(name=b["name"], defaults=b)
        branch_objects.append(obj)
        if created:
            print(f"  ✅ Создан филиал: {b['name']}")
    print(f"  📊 Всего филиалов: {Branch.objects.count()}")
    
    # ========== 2. ВИДЫ СТРАХОВАНИЯ ==========
    print("\n2. Проверка видов страхования...")
    types = [
        {"name": "Страхование автомобиля", "commission_percent": 10.00, "tariff_rate": 8.50},
        {"name": "Страхование имущества", "commission_percent": 12.00, "tariff_rate": 5.00},
        {"name": "Медицинское страхование", "commission_percent": 8.00, "tariff_rate": 12.00},
        {"name": "Страхование жизни", "commission_percent": 15.00, "tariff_rate": 15.00},
        {"name": "Страхование путешествий", "commission_percent": 7.00, "tariff_rate": 7.00},
        {"name": "Страхование от несчастных случаев", "commission_percent": 9.00, "tariff_rate": 4.00},
    ]
    
    type_objects = []
    for t in types:
        obj, created = InsuranceType.objects.get_or_create(name=t["name"], defaults=t)
        type_objects.append(obj)
        if created:
            print(f"  ✅ Создан вид: {t['name']}")
    print(f"  📊 Всего видов: {InsuranceType.objects.count()}")
    
    # ========== 3. СОТРУДНИКИ (АГЕНТЫ) ==========
    print("\n3. Проверка сотрудников...")
    agents = [
        {"full_name": "Иванова Анна Петровна", "position": "agent", "phone": "+375 (29) 111-11-11", "email": "anna@insurance.by"},
        {"full_name": "Петров Сергей Игоревич", "position": "agent", "phone": "+375 (29) 222-22-22", "email": "sergey@insurance.by"},
        {"full_name": "Сидорова Елена Владимировна", "position": "agent", "phone": "+375 (29) 333-33-33", "email": "elena@insurance.by"},
    ]
    
    agent_objects = []
    for a in agents:
        obj, created = StaffMember.objects.get_or_create(
            full_name=a["full_name"],
            defaults={
                "position": "agent",
                "department": "Продажи",
                "phone": a["phone"],
                "email": a["email"],
                "hire_date": date(2020, 1, 1),
                "is_active": True,
                "order": len(agent_objects) + 1
            }
        )
        agent_objects.append(obj)
        if created:
            print(f"  ✅ Создан сотрудник: {a['full_name']}")
    print(f"  📊 Всего сотрудников-агентов: {StaffMember.objects.filter(position='agent').count()}")
    
    # ========== 4. КЛИЕНТЫ ==========
    print("\n4. Генерация клиентов...")
    first_names = ["Иван", "Мария", "Дмитрий", "Ольга", "Алексей", "Екатерина", "Сергей", "Анна"]
    last_names = ["Петров", "Сидорова", "Козлов", "Новикова", "Морозов", "Волкова", "Иванов", "Соколова"]
    
    clients = []
    for i in range(20):  # 20 клиентов
        f_name = random.choice(first_names)
        l_name = random.choice(last_names)
        passport = f"AB{random.randint(1000000, 9999999)}"
        
        client, created = Client.objects.get_or_create(
            passport_number=passport,
            defaults={
                "first_name": f_name,
                "last_name": l_name,
                "middle_name": f"{f_name}овна" if l_name.endswith('а') else f"{f_name}ович",
                "address": f"г. Минск, ул. Примерная, {random.randint(1, 100)}",
                "phone": f"+375 (29) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}",
                "email": f"{f_name.lower()}.{l_name.lower()}@mail.com",
                "birth_date": date(random.randint(1970, 2005), random.randint(1, 12), random.randint(1, 28)),
            }
        )
        clients.append(client)
        if i < 5:
            print(f"  ✅ Создан клиент: {client}")
    print(f"  📊 Всего клиентов: {Client.objects.count()}")
    
    # ========== 5. ОБЪЕКТЫ СТРАХОВАНИЯ ==========
    print("\n5. Генерация объектов страхования...")
    object_types = ['car', 'property', 'health', 'life', 'travel']
    object_names = {
        'car': ['Toyota Camry', 'BMW X5', 'Audi A6', 'Mercedes E-Class', 'Volkswagen Golf'],
        'property': ['Квартира', 'Дом', 'Дача', 'Офис', 'Склад'],
        'health': ['ДМС стандарт', 'ДМС расширенный', 'Стоматология', 'Лечение за границей'],
        'life': ['Страхование жизни', 'Накопительное страхование', 'Пенсионная программа'],
        'travel': ['Страховка в Турцию', 'Страховка в Европу', 'Страховка в Азию']
    }
    
    for client in clients[:15]:  # Для 15 клиентов
        obj_type = random.choice(object_types)
        obj_name = random.choice(object_names[obj_type])
        InsuredObject.objects.get_or_create(
            client=client,
            object_type=obj_type,
            defaults={
                "description": obj_name,
                "value": Decimal(random.randint(10000, 500000))
            }
        )
    print(f"  📊 Всего объектов: {InsuredObject.objects.count()}")
    
    # ========== 6. ДОГОВОРЫ (основные данные для статистики) ==========
    print("\n6. Генерация договоров...")
    
    # Очищаем старые договоры (опционально)
    # InsuranceContract.objects.all().delete()
    
    start_date = date(2025, 1, 1)
    end_date = date(2026, 5, 31)
    current_date = start_date
    
    contracts_created = 0
    month_data = {}
    
    while current_date <= end_date:
        # Количество договоров в месяц (от 2 до 15)
        contracts_in_month = random.randint(2, 15)
        
        for _ in range(contracts_in_month):
            client = random.choice(clients)
            agent = random.choice(agent_objects)
            branch = random.choice(branch_objects)
            ins_type = random.choice(type_objects)
            
            # Стоимость и сумма
            object_value = Decimal(random.randint(50000, 500000))
            insurance_sum = object_value * Decimal(random.uniform(0.5, 1.0))
            tariff_rate = ins_type.tariff_rate
            
            # Случайная дата в текущем месяце
            day = random.randint(1, 28)
            contract_date = date(current_date.year, current_date.month, day)
            
            # Создаём договор
            contract = InsuranceContract(
                client=client,
                agent=agent,
                branch=branch,
                insurance_type=ins_type,
                insurance_sum=insurance_sum,
                tariff_rate=tariff_rate,
                start_date=contract_date,
                end_date=contract_date + timedelta(days=365),
                status='active'
            )
            contract.save()
            contracts_created += 1
            
            # Собираем статистику по месяцам
            month_key = contract_date.strftime('%Y-%m')
            if month_key not in month_data:
                month_data[month_key] = {'count': 0, 'sum': 0}
            month_data[month_key]['count'] += 1
            month_data[month_key]['sum'] += float(insurance_sum)
        
        # Переход к следующему месяцу
        if current_date.month == 12:
            current_date = date(current_date.year + 1, 1, 1)
        else:
            current_date = date(current_date.year, current_date.month + 1, 1)
    
    print(f"  ✅ Создано договоров: {contracts_created}")
    
    # ========== 7. ОТЗЫВЫ ==========
    print("\n7. Генерация отзывов...")
    review_texts = [
        "Отличная компания! Всё быстро и качественно.",
        "Хороший сервис, но немного долго оформляли документы.",
        "Профессиональные сотрудники, всё объяснили.",
        "Страховка помогла в трудной ситуации, спасибо!",
        "Рекомендую! Быстрое урегулирование убытков.",
        "Нормальная компания, но могли бы быть скидки.",
        "Всё понравилось, буду рекомендовать друзьям.",
        "Долго ждал выплату, но в итоге получил.",
    ]
    
    for client in clients[:10]:
        rating = random.randint(3, 5)
        text = random.choice(review_texts)
        Review.objects.get_or_create(
            client=client,
            defaults={
                "rating": rating,
                "text": text,
                "is_published": True
            }
        )
    print(f"  📊 Всего отзывов: {Review.objects.count()}")
    
    # ========== 8. ПРОМОКОДЫ ==========
    print("\n8. Генерация промокодов...")
    from django.utils import timezone
    promos = [
        {"code": "WELCOME10", "discount": 10},
        {"code": "SUMMER20", "discount": 20},
        {"code": "AUTUMN15", "discount": 15},
        {"code": "WINTER25", "discount": 25},
        {"code": "NEWYEAR30", "discount": 30},
    ]
    
    now = timezone.now()
    for p in promos:
        PromoCode.objects.get_or_create(
            code=p["code"],
            defaults={
                "discount_percent": p["discount"],
                "valid_from": now - timedelta(days=30),
                "valid_to": now + timedelta(days=60),
                "is_active": True,
                "max_uses": 100
            }
        )
    print(f"  📊 Всего промокодов: {PromoCode.objects.count()}")
    
    # ========== 9. НОВОСТИ ==========
    print("\n9. Генерация новостей...")
    news_titles = [
        "Новая программа страхования жизни",
        "Скидки для новых клиентов до 20%",
        "Открытие нового филиала в Гродно",
        "Мы стали лидерами рынка страхования",
        "Запуск мобильного приложения",
    ]
    
    for title in news_titles:
        News.objects.get_or_create(
            title=title,
            defaults={
                "short_description": f"Кратко о {title.lower()}",
                "content": f"Полное описание: {title.lower()}. Подробности уточняйте в офисе.",
                "is_published": True
            }
        )
    print(f"  📊 Всего новостей: {News.objects.count()}")
    
    # ========== 10. FAQ ==========
    print("\n10. Генерация FAQ...")
    faqs = [
        {"q": "Как оформить страховку?", "a": "Обратитесь в любой филиал с паспортом."},
        {"q": "Какие документы нужны?", "a": "Паспорт и документы на объект страхования."},
        {"q": "Как получить выплату?", "a": "Подайте заявление в филиале."},
        {"q": "Сколько времени занимает выплата?", "a": "До 30 дней с момента подачи заявления."},
    ]
    
    for f in faqs:
        FAQ.objects.get_or_create(
            question=f["q"],
            defaults={"answer": f["a"], "is_published": True}
        )
    print(f"  📊 Всего FAQ: {FAQ.objects.count()}")
    
    # ========== 11. ИТОГ ==========
    print("\n" + "=" * 60)
    print("ИТОГОВАЯ СТАТИСТИКА:")
    print("=" * 60)
    print(f"  ✅ Филиалы:              {Branch.objects.count()}")
    print(f"  ✅ Виды страхования:     {InsuranceType.objects.count()}")
    print(f"  ✅ Страховые агенты:     {StaffMember.objects.filter(position='agent').count()}")
    print(f"  ✅ Клиенты:              {Client.objects.count()}")
    print(f"  ✅ Объекты страхования:  {InsuredObject.objects.count()}")
    print(f"  ✅ Договоры:             {InsuranceContract.objects.count()}")
    print(f"  ✅ Отзывы:               {Review.objects.count()}")
    print(f"  ✅ Промокоды:            {PromoCode.objects.count()}")
    print(f"  ✅ Новости:              {News.objects.count()}")
    print(f"  ✅ FAQ:                  {FAQ.objects.count()}")
    print("=" * 60)
    
    # Выводим статистику по месяцам
    print("\n📊 ДИНАМИКА ПО МЕСЯЦАМ:")
    print("-" * 40)
    for month in sorted(month_data.keys()):
        data = month_data[month]
        print(f"  {month}: {data['count']} договоров на сумму {data['sum']:,.0f} руб.")
    print("=" * 60)
    
    print("\n🎉 ГЕНЕРАЦИЯ ДАННЫХ ЗАВЕРШЕНА!")

if __name__ == "__main__":
    # Импортируем модели внутри функции, чтобы избежать ошибок
    from core.models import Review, PromoCode, News, FAQ
    generate_test_data()