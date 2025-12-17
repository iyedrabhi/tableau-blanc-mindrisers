import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_project.settings')

app = Celery('restaurant_project')

# Load config from Django settings, CELERY_ namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks in installed apps
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
