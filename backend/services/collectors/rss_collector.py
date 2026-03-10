from intelligence.models import Source, RawData
from scrapers.rss_scraper import scrape_rss


def collect_rss_news():

    sources = Source.objects.filter(source_type="news")

    for source in sources:

        articles = scrape_rss(source.url)

        for article in articles:

            RawData.objects.get_or_create(
                source=source,
                url=article["url"],
                defaults={
                    "title": article["title"],
                    "content": article["content"]
                }
)