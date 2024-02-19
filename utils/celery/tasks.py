# add celery tasks here

import asyncio
from django.db.models import Q
from django.conf import settings

# custom
import telegram
from celery import shared_task
from news import models


@shared_task
def fetch_news():
    """
    filters all the selected / active websites, and fetches headlines
    """

    websites = models.Website.objects.filter(
        Q(is_active=True)
    )

    for instance in websites:
        instance.scrape_headlines()


async def send_message(title: str, source: str, sentiment: str):
    if not source:
        source = ''
    msg = '*' + title + '*' + \
        '\n\n' + f'Prediction : {sentiment}' + '\n\n' + \
        f'[Read full News]({source})'
    bot = telegram.Bot(token=settings.TELEGRAM_API_KEY)
    await bot.send_message(chat_id=settings.TELEGRAM_CHANNEL_ID, text=msg, parse_mode='markdown')


@shared_task
def send_news_to_telegram():
    """
    send news to telegram channel
    """
    
    active_news_instances = models.News.objects.filter(
        Q(is_active=True)
    ).order_by('id')

    if not active_news_instances.exists():
        print('[INFO] no active news found')
    else:
        news_instance = active_news_instances.first()

        asyncio.run(send_message(
                title=news_instance.title,
                source=news_instance.source,
                sentiment=news_instance.metadata.get('sentiment', 'Unpredictable')
            )
        )
        news_instance.is_active = False
        news_instance.save()
