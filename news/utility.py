import bs4
import requests

# custom
from . import models
from utils import helpers


class Scraper:
    """
    Used to extract news from different websites
    Every website, has a different scraping flow, thus create different functions

    Note:
    if name of website is 'Business Today',
    the function can be named as 'business_today'.
    It will be automatically mapped while calling the scrapper function, internally.
    """

    @staticmethod
    def business_today(url):
        response = requests.get(
            url=url
        )
        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        news_container = soup.find('div', 'section-listing-LHS')
        news_list = news_container.find_all('div', 'widget-listing')

        for target in news_list:
            target_content = target.find('h2').find('a').text
            target_source_url = target.find('h2').find('a')['href']

            sentiment = helpers.get_sentiment(text=target_content)
            _metadata = {
                'sentiment': sentiment
            }
            news_instance, created = models.News.objects.get_or_create(
                title=target_content,
                source=target_source_url,
                metadata=_metadata
            )
