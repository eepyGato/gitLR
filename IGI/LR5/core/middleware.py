# core/middleware.py
import requests
from django.utils import timezone
import pytz

def get_user_timezone(request):
    """Определяем часовой пояс по IP пользователя"""
    # Получаем IP пользователя
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    print(f"Определён IP: {ip}")
    
    # Определяем часовой пояс по IP (бесплатный API)
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        data = response.json()

        print(f"Ответ API: {data}")

        if data['status'] == 'success':
            return data['timezone']
    except:
        pass
    
    return 'Europe/Minsk'


class TimezoneMiddleware:
    """Middleware для установки часового пояса пользователя"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        tzname = get_user_timezone(request)
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)