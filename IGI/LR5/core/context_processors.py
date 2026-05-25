# core/context_processors.py
from django.utils import timezone


def site_info(request):
    """Context processor to add site-wide information"""
    now_utc = timezone.now()
    now_local = timezone.localtime(now_utc)  #UTC into local
    
    return {
        'current_year': now_local.year,
        'current_date_user_tz': now_local.strftime('%d/%m/%Y'),
        'current_datetime_user_tz': now_local.strftime('%d/%m/%Y %H:%M:%S'),
        'current_datetime_utc': now_utc.strftime('%d/%m/%Y %H:%M:%S'),
        'current_timezone': timezone.get_current_timezone_name(),
    }