import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogproject.settings")
django.setup()
from django.contrib.auth.models import User
try:
    admin = User.objects.get(username='law')
except:
    User.objects.create_superuser('law', 'law@exqopen.cn', 'blog64307822')
