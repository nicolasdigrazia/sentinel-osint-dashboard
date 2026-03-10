import feedparser


def scrape_rss(url):

    feed = feedparser.parse(url)

    news = []

    for entry in feed.entries:

        news.append({
            "title": entry.get("title", ""),
            "url": entry.get("link", ""),
            "content": entry.get("summary", "")
        })

    return news