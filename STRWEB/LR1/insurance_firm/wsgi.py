# insurance_firm/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insurance_firm.settings')
application = get_wsgi_application()