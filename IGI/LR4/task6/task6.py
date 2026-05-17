# ---------------------------------------------------------
# Lab Work №4 - Task 6 (Variant 27 - Sberbank Housing)
# Module: task6.py
# Purpose: Main program for Pandas analysis
# Version: 1.0
# Developer: Student
# Date of Development: 2026-05-17
# ---------------------------------------------------------

import pandas as pd
import numpy as np
from task6.pandas_analyzer import PandasBasics, HousingAnalyzer
from utils.inputValidator import input_data, input_with_validator

TASK_DESCRIPTION = r"""
╔══════════════════════════════════════════════════════════════════════╗
║                  ЗАДАНИЕ 6 - ВАРИАНТ 27 (СБЕРБАНК HOUSING)            ║
║                                                                       ║
║  ЗАДАНИЕ А: Библиотека Pandas. Структуры Series и DataFrame           ║
║  -------------------------------------------------------------------  ║
║  1. Импорт библиотеки Pandas                                          ║
║  2. Структура Series                                                  ║
║  3. Создание Series                                                   ║
║  4. Функция display                                                   ║
║  5. Доступ к элементам Series (.loc и .iloc)                          ║
║  6. Объект DataFrame. Создание                                        ║
║                                                                       ║
║  ЗАДАНИЕ Б: Основные операции и статистический анализ                 ║
║  -------------------------------------------------------------------  ║
║  1. Получение информации о датафрейме (по каждому параметру)          ║
║  2. Создать DataFrame из 5 случайных транзакций                       ║
║     (столбцы: цена, площадь, этаж)                                    ║
║  3. Сбросить индекс и сохранить старый как отдельный столбец          ║
║  4. Определить отношение средней цены за кв.м.                        ║
║     в дорогих районах к дешёвым (округлить до сотых)                  ║
╚══════════════════════════════════════════════════════════════════════╝
"""


def print_task_description():
    """Вывод описания задания"""
    print(TASK_DESCRIPTION)


def load_housing_data():
    """
    Загрузка данных по недвижимости (Sberbank Housing)
    Если реальный датасет не найден, создаётся тестовый
    """
    import os
    
    print("\n" + "-" * 50)
    print("ЗАГРУЗКА ДАННЫХ")
    print("-" * 50)
    
    # Предлагаем пользователю ввести путь к файлу
    print("\nВозможные варианты:")
    print("  1. Использовать встроенные тестовые данные")
    print("  2. Указать путь к CSV файлу")
    
    choice = input_data("Выберите вариант (1 или 2): ", int, min_value=1, max_value=2)
    
    if choice == 2:
        filepath = input_with_validator(
            "Введите путь к CSV файлу: ",
            lambda x: len(x) > 0
        )
        
        if os.path.exists(filepath):
            try:
                df = pd.read_csv(filepath)
                print(f"✓ Загружен датасет: {filepath}")
                print(f"  Размер: {df.shape[0]} строк, {df.shape[1]} столбцов")
                return df
            except Exception as e:
                print(f"✗ Ошибка при загрузке: {e}")
                print("  Будут использованы тестовые данные...")
        else:
            print(f"✗ Файл не найден: {filepath}")
            print("  Будут использованы тестовые данные...")
    
    # Создаём тестовые данные
    return create_test_housing_data()


def create_test_housing_data(n: int = 500):
    """
    Создание тестовых данных по недвижимости
    
    Args:
        n (int): Количество записей
        
    Returns:
        pd.DataFrame: Тестовые данные
    """
    np.random.seed(42)
    
    # Районы Москвы с разным уровнем цен
    districts = {
        'Arbat': 2.5, 'Khamovniki': 2.4, 'Tverskoy': 2.3, 'Presnensky': 2.2, 'Yakimanka': 2.2,
        'Zamoskvorechye': 1.9, 'Basmanny': 1.8, 'Meshchansky': 1.8, 'Tagansky': 1.7, 'Krasnoselsky': 1.6,
        'Danilovsky': 1.4, 'Donskoy': 1.3, 'Lefortovo': 1.2, 'Begovoy': 1.2, 'Dorogomilovo': 1.1,
        'Sokolniki': 1.0, 'Maryina Roshcha': 0.9, 'Ostankino': 0.9, 'Timiryazevsky': 0.8, 'Yuzhnoportovy': 0.7
    }
    
    base_price_per_sqm = 150000  # Базовая цена за кв.м.
    
    data = []
    for i in range(n):
        # Выбор района
        district = np.random.choice(list(districts.keys()))
        multiplier = districts[district]
        
        # Площадь (20-150 кв.м.)
        full_sq = np.random.uniform(25, 120)
        
        # Цена за кв.м. с учётом района и случайного шума
        price_per_sqm = base_price_per_sqm * multiplier * np.random.uniform(0.7, 1.3)
        price = price_per_sqm * full_sq * np.random.uniform(0.85, 1.15)
        
        # Этаж
        floor = np.random.randint(1, 26)
        max_floor = np.random.randint(5, 30)
        
        # Год постройки
        build_year = np.random.randint(1950, 2021)
        
        data.append({
            'price': int(price),
            'full_sq': round(full_sq, 1),
            'floor': floor,
            'max_floor': max_floor,
            'sub_area': district,
            'num_room': np.random.randint(1, 6),
            'build_year': build_year
        })
    
    df = pd.DataFrame(data)
    print(f"\n✓ Созданы тестовые данные: {n} записей")
    print(f"  Колонки: {list(df.columns)}")
    print(f"  Диапазон цен: {df['price'].min():,.0f} - {df['price'].max():,.0f} руб")
    
    return df


def task6() -> bool:
    """
    Главная функция задания 6
    
    Returns:
        bool: Всегда True для возврата в меню
    """
    print_task_description()
    
    while True:
        print("\n" + "=" * 70)
        print("МЕНЮ ЗАДАНИЯ 6 (ВАРИАНТ 27)")
        print("=" * 70)
        
        print("\n1. ЗАДАНИЕ А: Работа с Series и DataFrame")
        print("2. ЗАДАНИЕ Б: Анализ данных по недвижимости")
        print("3. Выполнить всё (А + Б)")
        print("4. Вернуться в главное меню")
        
        choice = input_data("\nВыберите опцию (1-4): ", int, min_value=1, max_value=4)
        
        if choice == 1:
            print("\n" + "▶ ВЫПОЛНЕНИЕ ЗАДАНИЯ А".center(70))
            PandasBasics.demonstrate_series()
            PandasBasics.demonstrate_dataframe()
            
        elif choice == 2:
            print("\n" + "▶ ВЫПОЛНЕНИЕ ЗАДАНИЯ Б".center(70))
            df = load_housing_data()
            if df is not None:
                analyzer = HousingAnalyzer(df)
                analyzer.run_all_tasks()
            else:
                print("✗ Не удалось загрузить данные!")
                
        elif choice == 3:
            print("\n" + "▶ ВЫПОЛНЕНИЕ ЗАДАНИЙ А И Б".center(70))
            
            # Задание А
            PandasBasics.demonstrate_series()
            PandasBasics.demonstrate_dataframe()
            
            # Задание Б
            df = load_housing_data()
            if df is not None:
                analyzer = HousingAnalyzer(df)
                analyzer.run_all_tasks()
            else:
                print("✗ Не удалось загрузить данные!")
                
        elif choice == 4:
            print("\n✓ Возврат в главное меню...\n")
            return True
        
        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    task6()