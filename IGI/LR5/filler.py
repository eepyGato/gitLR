# fill_database.py
import os
import django
from datetime import date, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insurance_firm.settings')
django.setup()

from core.models import (
    Branch, InsuranceType, Client, InsuranceContract, 
    News, FAQ, Vacancy, Review, PromoCode, StaffMember,
    CompanyInfo, CompanyHistory, InsuredObject
)

def fill_database():
    print("=" * 70)
    print("НАЧАЛО ЗАПОЛНЕНИЯ БАЗЫ ДАННЫХ")
    print("=" * 70)
    
    # ========== 1. ФИЛИАЛЫ ==========
    print("\n1. Добавление филиалов...")
    branches = [
        {"name": "Центральный офис", "address": "г. Минск, ул. Ленина, 1", "phone": "+375 (29) 111-11-11"},
        {"name": "Филиал на Немиге", "address": "г. Минск, ул. Немига, 10", "phone": "+375 (29) 222-22-22"},
        {"name": "Филиал на Победителей", "address": "г. Минск, пр. Победителей, 100", "phone": "+375 (29) 333-33-33"},
        {"name": "Филиал в Гродно", "address": "г. Гродно, ул. Советская, 15", "phone": "+375 (29) 444-44-44"},
        {"name": "Филиал в Бресте", "address": "г. Брест, ул. Московская, 20", "phone": "+375 (29) 555-55-55"},
        {"name": "Филиал в Витебске", "address": "г. Витебск, ул. Ленина, 5", "phone": "+375 (29) 666-66-66"},
        {"name": "Филиал в Могилёве", "address": "г. Могилёв, ул. Первомайская, 8", "phone": "+375 (29) 777-77-77"},
        {"name": "Филиал в Гомеле", "address": "г. Гомель, пр. Победы, 12", "phone": "+375 (29) 888-88-88"},
    ]
    for b in branches:
        Branch.objects.get_or_create(name=b["name"], defaults=b)
    print(f"   ✅ Создано филиалов: {Branch.objects.count()}")
    
    # ========== 2. ВИДЫ СТРАХОВАНИЯ ==========
    print("\n2. Добавление видов страхования...")
    types = [
        {"name": "Страхование автомобиля", "commission_percent": 10.00},
        {"name": "Страхование имущества", "commission_percent": 12.00},
        {"name": "Медицинское страхование", "commission_percent": 8.00},
        {"name": "Страхование жизни", "commission_percent": 15.00},
        {"name": "Страхование путешествий", "commission_percent": 7.00},
        {"name": "Страхование ответственности", "commission_percent": 11.00},
        {"name": "Страхование грузов", "commission_percent": 13.00},
        {"name": "Страхование бизнеса", "commission_percent": 14.00},
        {"name": "Страхование здоровья", "commission_percent": 8.50},
        {"name": "Страхование пенсии", "commission_percent": 5.00},
    ]
    for t in types:
        InsuranceType.objects.get_or_create(name=t["name"], defaults=t)
    print(f"   ✅ Создано видов страхования: {InsuranceType.objects.count()}")
    
    # ========== 3. СОТРУДНИКИ (включая агентов) ==========
    print("\n3. Добавление сотрудников...")
    staff_members = [
        {"full_name": "Иванова Анна Петровна", "position": "agent", "department": "Продажи",
         "phone": "+375 (29) 111-11-11", "email": "anna@insurance.by",
         "hire_date": date(2020, 1, 15), "is_active": True},
        {"full_name": "Петров Сергей Игоревич", "position": "manager", "department": "Продажи",
         "phone": "+375 (29) 222-22-22", "email": "sergey@insurance.by",
         "hire_date": date(2019, 3, 10), "is_active": True},
        {"full_name": "Сидорова Елена Владимировна", "position": "agent", "department": "Продажи",
         "phone": "+375 (29) 333-33-33", "email": "elena@insurance.by",
         "hire_date": date(2021, 6, 20), "is_active": True},
        {"full_name": "Козлов Дмитрий Андреевич", "position": "director", "department": "Управление",
         "phone": "+375 (29) 444-44-44", "email": "dmitry@insurance.by",
         "hire_date": date(2018, 1, 1), "is_active": True},
        {"full_name": "Новикова Ольга Сергеевна", "position": "accountant", "department": "Бухгалтерия",
         "phone": "+375 (29) 555-55-55", "email": "olga@insurance.by",
         "hire_date": date(2020, 9, 5), "is_active": True},
    ]
    for s in staff_members:
        StaffMember.objects.get_or_create(full_name=s["full_name"], defaults=s)
    print(f"   ✅ Создано сотрудников: {StaffMember.objects.count()}")
    print(f"   📌 Из них агентов: {StaffMember.objects.filter(position='agent').count()}")
    
    # ========== 4. КЛИЕНТЫ ==========
    print("\n4. Добавление клиентов...")
    clients = [
        {"first_name": "Иван", "last_name": "Петров", "middle_name": "Иванович",
         "address": "г. Минск, ул. Ленина, 10", "phone": "+375 (29) 123-45-67",
         "email": "ivan@mail.ru", "birth_date": date(1990, 5, 15), "passport_number": "AB1234567"},
        {"first_name": "Мария", "last_name": "Сидорова", "middle_name": "Петровна",
         "address": "г. Минск, ул. Немига, 15", "phone": "+375 (29) 234-56-78",
         "email": "maria@mail.ru", "birth_date": date(1992, 8, 20), "passport_number": "AC2345678"},
        {"first_name": "Дмитрий", "last_name": "Козлов", "middle_name": "Андреевич",
         "address": "г. Минск, пр. Победителей, 25", "phone": "+375 (29) 345-67-89",
         "email": "dmitry@mail.ru", "birth_date": date(1988, 3, 10), "passport_number": "AD3456789"},
        {"first_name": "Ольга", "last_name": "Новикова", "middle_name": "Сергеевна",
         "address": "г. Гродно, ул. Советская, 5", "phone": "+375 (29) 456-78-90",
         "email": "olga@mail.ru", "birth_date": date(1995, 11, 25), "passport_number": "AE4567890"},
        {"first_name": "Алексей", "last_name": "Морозов", "middle_name": "Викторович",
         "address": "г. Брест, ул. Московская, 30", "phone": "+375 (29) 567-89-01",
         "email": "alex@mail.ru", "birth_date": date(1991, 7, 5), "passport_number": "AF5678901"},
        {"first_name": "Екатерина", "last_name": "Волкова", "middle_name": "Алексеевна",
         "address": "г. Витебск, ул. Ленина, 12", "phone": "+375 (29) 678-90-12",
         "email": "ekaterina@mail.ru", "birth_date": date(1993, 2, 18), "passport_number": "AG6789012"},
    ]
    for c in clients:
        Client.objects.get_or_create(passport_number=c["passport_number"], defaults=c)
    print(f"   ✅ Создано клиентов: {Client.objects.count()}")
    
    # ========== 5. ОБЪЕКТЫ СТРАХОВАНИЯ ==========
    print("\n5. Добавление объектов страхования...")
    clients_list = list(Client.objects.all())
    objects_data = [
        {"client": clients_list[0], "object_type": "car", "description": "Toyota Camry 2020", "value": 45000},
        {"client": clients_list[1], "object_type": "property", "description": "Квартира в Минске", "value": 120000},
        {"client": clients_list[2], "object_type": "car", "description": "BMW X5 2019", "value": 60000},
        {"client": clients_list[3], "object_type": "health", "description": "ДМС расширенный", "value": 15000},
        {"client": clients_list[4], "object_type": "travel", "description": "Поездка в Турцию", "value": 3000},
        {"client": clients_list[5], "object_type": "life", "description": "Страхование жизни", "value": 50000},
    ]
    for obj in objects_data:
        InsuredObject.objects.get_or_create(
            client=obj["client"],
            object_type=obj["object_type"],
            defaults={"description": obj["description"], "value": obj["value"]}
        )
    print(f"   ✅ Создано объектов страхования: {InsuredObject.objects.count()}")
    
    # ========== 6. НОВОСТИ ==========
    print("\n6. Добавление новостей...")
    news_list = [
        {"title": "Новая программа страхования жизни", 
         "short_description": "Запущена программа с выгодными условиями",
         "content": "Мы рады сообщить о запуске новой программы страхования жизни...",
         "is_published": True},
        {"title": "Скидки для новых клиентов", 
         "short_description": "Специальное предложение до конца месяца",
         "content": "При оформлении страховки до конца месяца действует скидка 15%...",
         "is_published": True},
        {"title": "Открытие нового филиала", 
         "short_description": "Новый филиал в Гродно",
         "content": "Мы рады сообщить об открытии нового филиала в городе Гродно...",
         "is_published": True},
    ]
    for n in news_list:
        News.objects.get_or_create(title=n["title"], defaults=n)
    print(f"   ✅ Создано новостей: {News.objects.count()}")
    
    # ========== 7. FAQ ==========
    print("\n7. Добавление FAQ...")
    faqs = [
        {"question": "Как оформить страховку?", 
         "answer": "Обратитесь в любой наш филиал с паспортом", "is_published": True},
        {"question": "Какие документы нужны?", 
         "answer": "Паспорт и документы на объект страхования", "is_published": True},
        {"question": "Как получить выплату?", 
         "answer": "Подайте заявление в филиале с документами", "is_published": True},
        {"question": "Сколько времени занимает оформление?", 
         "answer": "Обычно 15-20 минут", "is_published": True},
    ]
    for f in faqs:
        FAQ.objects.get_or_create(question=f["question"], defaults=f)
    print(f"   ✅ Создано вопросов: {FAQ.objects.count()}")
    
    # ========== 8. ВАКАНСИИ ==========
    print("\n8. Добавление вакансий...")
    vacancies = [
        {"title": "Страховой агент", 
         "description": "Поиск клиентов, консультирование, заключение договоров",
         "requirements": "Опыт работы от 1 года", "salary_from": 1000, "salary_to": 3000,
         "location": "Минск", "is_active": True},
        {"title": "Менеджер по продажам", 
         "description": "Управление отделом продаж, обучение персонала",
         "requirements": "Опыт управления от 3 лет", "salary_from": 2000, "salary_to": 5000,
         "location": "Минск", "is_active": True},
        {"title": "Юрист", 
         "description": "Юридическое сопровождение договоров",
         "requirements": "Высшее юридическое образование", "salary_from": 1500, "salary_to": 3500,
         "location": "Минск", "is_active": True},
    ]
    for v in vacancies:
        Vacancy.objects.get_or_create(title=v["title"], defaults=v)
    print(f"   ✅ Создано вакансий: {Vacancy.objects.count()}")
    
    # ========== 9. ОТЗЫВЫ ==========
    print("\n9. Добавление отзывов...")
    clients_list = list(Client.objects.all())
    reviews = [
        {"client": clients_list[0], "rating": 5, "text": "Отличная компания! Быстро оформил страховку."},
        {"client": clients_list[1], "rating": 4, "text": "Хороший сервис, но немного долго ждала документы."},
        {"client": clients_list[2], "rating": 5, "text": "Профессиональные сотрудники, всё сделали оперативно."},
    ]
    for r in reviews:
        Review.objects.get_or_create(client=r["client"], defaults=r)
    print(f"   ✅ Создано отзывов: {Review.objects.count()}")
    
    # ========== 10. ПРОМОКОДЫ ==========
    print("\n10. Добавление промокодов...")
    now = timezone.now()
    promos = [
        {"code": "WELCOME10", "discount_percent": 10.00, "valid_from": now, 
         "valid_to": now + timedelta(days=30), "is_active": True},
        {"code": "SUMMER20", "discount_percent": 20.00, "valid_from": now, 
         "valid_to": now + timedelta(days=60), "is_active": True},
        {"code": "AUTUMN15", "discount_percent": 15.00, "valid_from": now, 
         "valid_to": now + timedelta(days=45), "is_active": True},
    ]
    for p in promos:
        PromoCode.objects.get_or_create(code=p["code"], defaults=p)
    print(f"   ✅ Создано промокодов: {PromoCode.objects.count()}")
    
    # ========== 11. ИНФОРМАЦИЯ О КОМПАНИИ ==========
    print("\n11. Добавление информации о компании...")
    company_info, created = CompanyInfo.objects.get_or_create(
        name="ООО 'Страховая фирма'",
        defaults={
            "short_description": "Лидер страхового рынка Беларуси с 1998 года",
            "full_description": "Мы предоставляем полный спектр страховых услуг...",
            "foundation_year": 1998,
            "ceo_name": "Петров Иван Сергеевич",
            "employees_count": 150,
            "legal_address": "г. Минск, ул. Ленина, 1",
            "actual_address": "г. Минск, ул. Ленина, 1",
            "inn": "123456789",
            "ogrn": "1123456789012",
            "bank_name": "Приорбанк",
            "bank_account": "BY12345678901234567890",
            "bik": "PJBY123456",
        }
    )
    print(f"   ✅ Информация о компании {'добавлена' if created else 'уже существует'}")
    
    # ========== 12. ИСТОРИЯ КОМПАНИИ ==========
    print("\n12. Добавление истории компании...")
    history = [
        {"year": 1998, "title": "Основание компании", "description": "Компания основана как ООО 'Страховая фирма'", "order": 1},
        {"year": 2005, "title": "Начало работы в регионах", "description": "Открыты филиалы в Гродно, Бресте, Витебске", "order": 2},
        {"year": 2015, "title": "Лидер рынка", "description": "Компания признана лидером страхового рынка", "order": 3},
        {"year": 2020, "title": "Цифровая трансформация", "description": "Запущена онлайн-платформа", "order": 4},
    ]
    for h in history:
        CompanyHistory.objects.get_or_create(year=h["year"], title=h["title"], defaults=h)
    print(f"   ✅ Создано записей истории: {CompanyHistory.objects.count()}")
    
    # ========== ИТОГ ==========
    print("\n" + "=" * 70)
    print("ИТОГ ЗАПОЛНЕНИЯ БАЗЫ ДАННЫХ:")
    print("=" * 70)
    print(f"   ✅ Филиалы:                    {Branch.objects.count()}")
    print(f"   ✅ Виды страхования:           {InsuranceType.objects.count()}")
    print(f"   ✅ Сотрудники:                 {StaffMember.objects.count()}")
    print(f"   ✅ Клиенты:                    {Client.objects.count()}")
    print(f"   ✅ Объекты страхования:        {InsuredObject.objects.count()}")
    print(f"   ✅ Новости:                    {News.objects.count()}")
    print(f"   ✅ FAQ:                        {FAQ.objects.count()}")
    print(f"   ✅ Вакансии:                   {Vacancy.objects.count()}")
    print(f"   ✅ Отзывы:                     {Review.objects.count()}")
    print(f"   ✅ Промокоды:                  {PromoCode.objects.count()}")
    print(f"   ✅ История компании:           {CompanyHistory.objects.count()}")
    print("=" * 70)
    print("\n🎉 БАЗА ДАННЫХ УСПЕШНО ЗАПОЛНЕНА!")

if __name__ == "__main__":
    fill_database()