from intelligence.models import Source, RawData
from intelligence.scrapers.rss_scraper import scrape_rss
from intelligence.services.analysis.pipeline import NLPPipeline
import datetime


def collect_rss_news():

    sources = Source.objects.filter(source_type="news")
    pipeline = NLPPipeline()

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

            raw_data, created = RawData.objects.get_or_create(
                url=article["url"],
                defaults={
                    "source": source,
                    "title": article["title"],
                    "category": source.category,
                    "content": article["content"],
                    "published_at": published_at,
                }
            )

            if created:
                try:
                    pipeline.analyze(raw_data)
                    raw_data.processed = True
                    raw_data.save()
                except Exception as e:
                    print(f"Error analizando RawData #{raw_data.id}: {e}")