from services.collectors.rss_collector import collect_rss_news


def run():
    print("Recolectando noticias...")
    collect_rss_news()
    print("Done.")
