from django.db import models

# custom
from .utility import Scraper


class Website(models.Model):

    name = models.CharField(max_length=299, help_text='name it in lower case, seperated by spaces (min 2 words)')
    url = models.URLField()
    metadata = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def scrape_headlines(self):
        '''
        maps the website name, with method defined in Scraper class
        and returns it
        '''
        scraper_instance = Scraper()

        arr = self.name.split()
        event_handler_name = '_'.join(arr)
        event_handler = getattr(scraper_instance, event_handler_name, None)
        if event_handler: return event_handler(self.url)
        raise Exception(f'Event handler for {self.name} not found')


class News(models.Model):

    title = models.CharField(max_length=999)
    source = models.URLField(blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title[:100]
    