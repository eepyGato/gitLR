# ---------------------------------------------------------
# Lab Work №4 - Task 6 (Variant 27 - Sberbank Housing)
# Module: pandas_analyzer.py
# Purpose: Pandas Series and DataFrame Analysis Classes
# Version: 1.0
# Developer: Student
# Date of Development: 2026-05-17
# ---------------------------------------------------------

import pandas as pd
import numpy as np
from IPython.display import display


class PandasBasics:
    """
    ЗАДАНИЕ А: Библиотека Pandas. Структуры Series и DataFrame
    1. Импорт библиотеки
    2. Структура Series
    3. Создание Series
    4. Функция display
    5. Доступ к элементам Series с использованием .loc или .iloc
    6. Объект DataFrame. Создание
    """

    @staticmethod
    def demonstrate_series():
        """Демонстрация работы с Series"""
        print("\n" + "=" * 70)
        print("ЗАДАНИЕ А: РАБОТА С SERIES")
        print("=" * 70)
        
        # 2. Структура Series
        print("\n1. Создание Series из списка:")
        series1 = pd.Series([10, 20, 30, 40, 50])
        display(series1)
        
        # 3. Создание Series с пользовательским индексом
        print("\n2. Создание Series с пользовательским индексом:")
        series2 = pd.Series([100, 200, 300, 400, 500], 
                           index=['a', 'b', 'c', 'd', 'e'])
        display(series2)
        
        # 4. Функция display уже используется выше
        
        # 5. Доступ к элементам с .loc и .iloc
        print("\n3. Доступ к элементам Series:")
        print(f"   .loc['c']: {series2.loc['c']}")
        print(f"   .iloc[2]: {series2.iloc[2]}")
        print(f"   .loc['b':'d']:\n{series2.loc['b':'d']}")
        print(f"   .iloc[1:4]:\n{series2.iloc[1:4]}")
        
        return series2

    @staticmethod
    def demonstrate_dataframe():
        """Демонстрация работы с DataFrame"""
        print("\n" + "=" * 70)
        print("ЗАДАНИЕ А: РАБОТА С DATAFRAME")
        print("=" * 70)
        
        # 6. Создание DataFrame
        print("\n1. Создание DataFrame из словаря:")
        df = pd.DataFrame({
            'price': [7500000, 5200000, 8900000, 4300000, 11200000],
            'full_sq': [65.5, 42.0, 78.2, 48.0, 95.0],
            'floor': [5, 3, 12, 1, 15],
            'sub_area': ['Paveletsky', 'Presnensky', 'Arbat', 'Yuzhnoportovy', 'Khamovniki']
        })
        display(df)
        
        print("\n2. Информация о DataFrame:")
        print(f"   Форма: {df.shape}")
        print(f"   Индексы: {df.index.tolist()}")
        print(f"   Колонки: {df.columns.tolist()}")
        
        print("\n3. Доступ к колонкам:")
        print(f"   df['price']:\n{df['price']}")
        print(f"\n   df[['price', 'full_sq']]:")
        display(df[['price', 'full_sq']])
        
        print("\n4. Доступ к строкам:")
        print(f"   df.loc[2]:\n{df.loc[2]}")
        print(f"\n   df.iloc[2]:\n{df.iloc[2]}")
        print(f"\n   df.loc[1:3]:")
        display(df.loc[1:3])
        
        return df


class HousingAnalyzer:
    """
    ЗАДАНИЕ Б: Основные операции и статистический анализ
    Вариант 27 - Сбербанк Housing
    
    Задачи:
    1. Создать DataFrame из 5 случайных транзакций (price, full_sq, floor)
    2. Сбросить индекс и сохранить старый как отдельный столбец
    3. Определить отношение средней цены за кв.м. в дорогих районах к дешёвым
    """

    def __init__(self, df: pd.DataFrame):
        """Инициализация с DataFrame"""
        self.df = df.copy()
        self.original_df = df.copy()

    def get_dataframe_info(self):
        """
        Получение информации о датафрейме (по каждому параметру)
        """
        print("\n" + "=" * 70)
        print("ЗАДАНИЕ Б: ИНФОРМАЦИЯ О ДАТАФРЕЙМЕ")
        print("=" * 70)
        
        print(f"\n1. Общая информация:")
        print(f"   Количество строк: {self.df.shape[0]}")
        print(f"   Количество столбцов: {self.df.shape[1]}")
        print(f"   Имена столбцов: {list(self.df.columns)}")
        
        print(f"\n2. Типы данных:")
        print(self.df.dtypes)
        
        print(f"\n3. Статистика по числовым столбцам:")
        display(self.df.describe())
        
        print(f"\n4. Информация о пропущенных значениях:")
        print(self.df.isnull().sum())
        
        print(f"\n5. Первые 5 строк:")
        display(self.df.head())
        
        print(f"\n6. Последние 5 строк:")
        display(self.df.tail())

    def task1_create_sample(self, n: int = 5):
        """
        ЗАДАЧА 1: Создать DataFrame из n случайных транзакций
        Оставить столбцы: цена, площадь, этаж
        
        Args:
            n (int): Количество случайных транзакций
            
        Returns:
            pd.DataFrame: DataFrame с выбранными столбцами
        """
        print("\n" + "=" * 70)
        print("ЗАДАНИЕ Б - ЗАДАЧА 1: ВЫБОРКА СЛУЧАЙНЫХ ТРАНЗАКЦИЙ")
        print("=" * 70)
        
        if len(self.df) < n:
            print(f"Предупреждение: В датасете только {len(self.df)} строк. Использую все.")
            n = len(self.df)
        
        # Выборка случайных строк
        sample = self.df.sample(n=n, random_state=42)
        
        # Оставляем нужные столбцы
        required_cols = ['price', 'full_sq', 'floor']
        available_cols = [col for col in required_cols if col in sample.columns]
        
        if len(available_cols) < 3:
            print(f"Предупреждение: Не все столбцы найдены. Найдено: {available_cols}")
        
        result = sample[available_cols].copy()
        
        print(f"\nСоздан DataFrame из {len(result)} случайных транзакций:")
        print(f"Столбцы: {list(result.columns)}")
        display(result)
        
        return result

    def task2_reset_index_with_save(self, df: pd.DataFrame):
        """
        ЗАДАЧА 2: Сбросить индекс и сохранить старый как отдельный столбец
        
        Args:
            df (pd.DataFrame): DataFrame для обработки
            
        Returns:
            pd.DataFrame: DataFrame со сброшенным индексом
        """
        print("\n" + "=" * 70)
        print("ЗАДАНИЕ Б - ЗАДАЧА 2: СБРОС ИНДЕКСА С СОХРАНЕНИЕМ")
        print("=" * 70)
        
        print("\nИсходный DataFrame:")
        display(df)
        
        print(f"\nИсходный индекс: {df.index.tolist()}")
        
        # Сброс индекса с сохранением старого
        result = df.reset_index()
        result = result.rename(columns={'index': 'old_index'})
        
        print(f"\nПосле сброса индекса:")
        print(f"Новый индекс: {result.index.tolist()}")
        print(f"Старый индекс сохранён в колонке 'old_index'")
        display(result)
        
        return result

    def task3_calculate_price_per_sqm_ratio(self):
        """
        ЗАДАЧА 3 (статистический анализ):
        Определить, во сколько раз средняя цена квадратного метра (price / full_sq)
        в самых дорогих районах (sub_area) больше, чем в самых дешевых районах.
        
        Ответ округлить до сотых.
        
        Returns:
            float: Отношение средних цен
        """
        print("\n" + "=" * 70)
        print("ЗАДАНИЕ Б - ЗАДАЧА 3: СТАТИСТИЧЕСКИЙ АНАЛИЗ")
        print("=" * 70)
        
        # Проверка наличия необходимых столбцов
        required_cols = ['price', 'full_sq', 'sub_area']
        for col in required_cols:
            if col not in self.df.columns:
                print(f"Ошибка: Столбец '{col}' не найден в датасете!")
                print(f"Доступные столбцы: {list(self.df.columns)}")
                return None
        
        # Расчёт цены за квадратный метр
        self.df['price_per_sqm'] = self.df['price'] / self.df['full_sq']
        
        print("\n1. Добавлен столбец 'price_per_sqm' (цена за кв.м.):")
        display(self.df[['price', 'full_sq', 'price_per_sqm', 'sub_area']].head())
        
        # Удаление выбросов (верхние и нижние 1% для корректности)
        lower_bound = self.df['price_per_sqm'].quantile(0.01)
        upper_bound = self.df['price_per_sqm'].quantile(0.99)
        clean_df = self.df[(self.df['price_per_sqm'] >= lower_bound) & 
                           (self.df['price_per_sqm'] <= upper_bound)]
        
        print(f"\n2. После удаления выбросов (1-99 перцентили):")
        print(f"   Было строк: {len(self.df)}")
        print(f"   Стало строк: {len(clean_df)}")
        
        # Группировка по районам и расчёт средней цены за кв.м.
        district_avg = clean_df.groupby('sub_area')['price_per_sqm'].mean().sort_values()
        
        print(f"\n3. Средняя цена за кв.м. по районам (от дешёвых к дорогим):")
        for district, price in district_avg.head(5).items():
            print(f"   {district}: {price:,.2f} руб/кв.м")
        print("   ...")
        for district, price in district_avg.tail(5).items():
            print(f"   {district}: {price:,.2f} руб/кв.м")
        
        # Поиск самого дорогого и самого дешёвого района
        richest_district = district_avg.idxmax()
        poorest_district = district_avg.idxmin()
        
        richest_avg = district_avg.max()
        poorest_avg = district_avg.min()
        
        # Расчёт отношения
        ratio = richest_avg / poorest_avg
        ratio_rounded = round(ratio, 2)
        
        print(f"\n4. Результаты анализа:")
        print(f"   Самый дорогой район: {richest_district}")
        print(f"   Средняя цена за кв.м.: {richest_avg:,.2f} руб/кв.м")
        print(f"\n   Самый дешёвый район: {poorest_district}")
        print(f"   Средняя цена за кв.м.: {poorest_avg:,.2f} руб/кв.м")
        print(f"\n   ОТНОШЕНИЕ (дорогой / дешёвый): {ratio_rounded}")
        
        return ratio_rounded

    def run_all_tasks(self):
        """
        Запуск всех задач для варианта 27
        """
        print("\n" + "█" * 70)
        print("ВЫПОЛНЕНИЕ ЗАДАНИЯ 6 ВАРИАНТ 27 (СБЕРБАНК HOUSING)")
        print("█" * 70)
        
        # Информация о датафрейме
        self.get_dataframe_info()
        
        # Задача 1: Создание выборки
        sample_df = self.task1_create_sample(5)
        
        # Задача 2: Сброс индекса с сохранением
        reset_df = self.task2_reset_index_with_save(sample_df)
        
        # Задача 3: Статистический анализ (отношение средних)
        ratio = self.task3_calculate_price_per_sqm_ratio()
        
        # Финальный ответ
        print("\n" + "=" * 70)
        print("ИТОГОВЫЙ ОТВЕТ ДЛЯ ВАРИАНТА 27")
        print("=" * 70)
        print(f"\n✓ Средняя цена квадратного метра в самых дорогих районах")
        print(f"  В {ratio} РАЗА выше, чем в самых дешёвых районах.")
        
        return {
            'sample_df': sample_df,
            'reset_df': reset_df,
            'ratio': ratio
        }