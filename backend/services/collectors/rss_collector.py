from intelligence.models import Source, RawData
from scrapers.rss_scraper import scrape_rss
import datetime


def collect_rss_news():

    sources = Source.objects.filter(source_type="news")

    for source in sources:

        articles = scrape_rss(source.url)

        for article in articles:

            published_at = None
            if article.get("published_parsed"):
                try:
                    published_at = datetime.datetime(
                        *article["published_parsed"][:6],
                        tzinfo=datetime.timezone.utc
                    )
                except:
                    pass

            RawData.objects.get_or_create(
                url=article["url"],
                defaults={
                    "source": source,
                    "title": article["title"],
                    "content": article["content"],
                    "published_at": published_at,
                }
            )