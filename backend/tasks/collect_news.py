from services.collectors.rss_collector import collect_rss_news


def run():

    print("Collecting RSS news...")

    collect_rss_news()

    print("Done.")