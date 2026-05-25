import os
import geometric_lib.square as square

# Получаем данные из переменной окружения, по умолчанию берем 10
side_length = int(os.environ.get('SIDE', 10))

area = square.area(side_length)
print(f"Сторона квадрата: {side_length}")
print(f"Площадь квадрата: {area}")