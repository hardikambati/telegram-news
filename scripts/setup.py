# internal imports
import subprocess

# django imports
from django.conf import settings
from django.contrib.auth import get_user_model
from django_celery_beat.models import (
    PeriodicTask,
    CrontabSchedule,
)

# custom imports
from utils.celery import tasks


User = get_user_model()
passed, failed = 0, 0
failed_messages = []


def migrate_db() -> None:
    global failed, passed, failed_messages
    try:
        subprocess.run(["python3", "manage.py", "migrate"])
        passed += 1
    except Exception as e:
        failed += 1
        failed_messages.append(str(e))


def create_superuser() -> None:
    global failed, passed, failed_messages
    
    superuser_info = {
        "username": "admin",
        "email": "admin@1.com",
        "password": "admin",
        "first_name": "test",
        "last_name": "test"
    }

    try:
        if not User.objects\
            .filter(username=superuser_info.get('username'))\
                .exists():
            User.objects.create_superuser(
                **superuser_info
            )
        passed += 1
    except Exception as e:
        failed_messages.append(str(e))
        failed += 1


def collect_static() -> None:
    global failed, passed, failed_messages
    try:
        subprocess.run(['python3', 'manage.py', 'collectstatic', '--no-input'])
        passed += 1
    except Exception as e:
        failed_messages.append(str(e))
        failed += 1


def fetch_news_periodic_task() -> None:
    global passed, failed
    try:
        name = 'Fetch and save news for every 3 minutes'
        
        if not PeriodicTask.objects.filter(name=name).exists():            
            crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
                minute='*/3',
            )
            PeriodicTask.objects.create(
                name=name,
                task='utils.celery.tasks.fetch_news',
                crontab=crontab_schedule
            )
        passed += 1
    except Exception as e:
        failed_messages.append(str(e))
        failed += 1


def send_telegram_message_periodic_task() -> None:
    global passed, failed
    try:
        name = 'Send message to telegram channel every 1 minute'
        if not PeriodicTask.objects.filter(name=name).exists():            
            crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
                minute='*/1',
            )
            PeriodicTask.objects.create(
                name=name,
                task='utils.celery.tasks.send_news_to_telegram',
                crontab=crontab_schedule
            )
        passed += 1
    except Exception as e:
        failed_messages.append(str(e))
        failed += 1


def run():
    print("performing setups...")

    migrate_db()
    create_superuser()
    fetch_news_periodic_task()
    send_telegram_message_periodic_task()

    if not settings.DEBUG:
        collect_static()

    print("setup complete")
    print(f"{passed} setups passed")
    print(f"{failed} setups failed")

    if len(failed_messages):
        print(f"failed messages - {failed_messages}")
