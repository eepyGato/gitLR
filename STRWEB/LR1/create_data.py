# create_data.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insurance_firm.settings')
django.setup()

from core.models import Branch, InsuranceType

def create_data():
    # Филиалы
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
        ]
        Branch.objects.bulk_create(branches)
        print(f"✅ Создано {Branch.objects.count()} филиалов")
    else:
        print(f"⚠️ Филиалы уже есть: {Branch.objects.count()}")
    
    # Виды страхования
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
        ]
        InsuranceType.objects.bulk_create(types)
        print(f"✅ Создано {InsuranceType.objects.count()} видов страхования")
    else:
        print(f"⚠️ Виды страхования уже есть: {InsuranceType.objects.count()}")

if __name__ == "__main__":
    create_data()