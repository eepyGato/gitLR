# insurance_firm/asgi.py
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insurance_firm.settings')
application = get_asgi_application()