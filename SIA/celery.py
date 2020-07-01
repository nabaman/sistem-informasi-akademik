import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SIA.settings')

app = Celery('SIA')
app.config_from_object('django.conf:settings',namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'create_absen_everyday_ganjil': {
        'task': 'dashboard.tasks.create_absen_ganjil',
        'schedule': crontab(minute=0,hour=1,day_of_week='1,2,3,4,5,6', month_of_year='1,2,3,4,5,6'),
    },
    'create_absen_everyday_genap': {
        'task': 'dashboard.tasks.create_absen_genap',
        'schedule': crontab(minute=0,hour=1,day_of_week='1,2,3,4,5,6', month_of_year='7,8,9,10,11,12'),
    },
}