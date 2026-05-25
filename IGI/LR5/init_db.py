# init_db.py
import os
import sys
import django

# Настройка Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insurance_firm.settings')
django.setup()

from core.models import Branch, InsuranceType

print("=" * 60)
print("Инициализация базы данных страховой компании")
print("=" * 60)

# Создаём филиалы
if Branch.objects.count() == 0:
    branches = [
        Branch(name="Центральный офис", address="г. Минск, ул. Ленина, 1", phone="+375 (29) 111-11-11"),
        Branch(name="Филиал на Немиге", address="г. Минск, ул. Немига, 10", phone="+375 (29) 222-22-22"),
        Branch(name="Филиал на Победителей", address="г. Минск, пр. Победителей, 100", phone="+375 (29) 333-33-33"),
        Branch(name="Филиал в Гродно", address="г. Гродно, ул. Советская, 15", phone="+375 (29) 444-44-44"),
        Branch(name="Филиал в Бресте", address="г. Брест, ул. Московская, 20", phone="+375 (29) 555-55-55"),
        Branch(name="Филиал в Витебске", address="г. Витебск, ул. Ленина, 5", phone="+375 (29) 666-66-66"),
        Branch(name="Филиал в Могилёве", address="г. Могилёв, ул. Первомайская, 8", phone="+375 (29) 777-77-77"),
        Branch(name="Филиал в Гомеле", address="г. Гомель, пр. Победы, 12", phone="+375 (29) 888-88-88"),
        Branch(name="Филиал в Бобруйске", address="г. Бобруйск, ул. Социалистическая, 30", phone="+375 (29) 999-99-99"),
        Branch(name="Филиал в Борисове", address="г. Борисов, ул. Ленинская, 25", phone="+375 (29) 101-01-01"),
    ]
    Branch.objects.bulk_create(branches)
    print(f"✅ Создано филиалов: {Branch.objects.count()}")
else:
    print(f"⚠️ Филиалы уже есть: {Branch.objects.count()}")

# Создаём виды страхования
if InsuranceType.objects.count() == 0:
    types = [
        InsuranceType(name="Страхование автомобиля", commission_percent=10.00),
        InsuranceType(name="Страхование имущества", commission_percent=12.00),
        InsuranceType(name="Медицинское страхование", commission_percent=8.00),
        InsuranceType(name="Страхование жизни", commission_percent=15.00),
        InsuranceType(name="Страхование путешествий", commission_percent=7.00),
        InsuranceType(name="Страхование от несчастных случаев", commission_percent=9.00),
        InsuranceType(name="Страхование ответственности", commission_percent=11.00),
        InsuranceType(name="Страхование грузов", commission_percent=13.00),
        InsuranceType(name="Страхование бизнеса", commission_percent=14.00),
        InsuranceType(name="Страхование урожая", commission_percent=6.00),
        InsuranceType(name="Страхование здоровья", commission_percent=8.50),
        InsuranceType(name="Страхование пенсии", commission_percent=5.00),
    ]
    InsuranceType.objects.bulk_create(types)
    print(f"✅ Создано видов страхования: {InsuranceType.objects.count()}")
else:
    print(f"⚠️ Виды страхования уже есть: {InsuranceType.objects.count()}")

print("\n" + "=" * 60)
print("📊 Итог в базе данных:")
print(f"  - Филиалы: {Branch.objects.count()}")
print(f"  - Виды страхования: {InsuranceType.objects.count()}")
print("=" * 60)