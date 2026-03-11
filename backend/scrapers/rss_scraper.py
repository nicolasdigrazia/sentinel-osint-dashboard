import feedparser
import re


def clean_html(text):
    text = re.sub("<.*?>", " ", text)
    text = re.sub("\s+", " ", text)
    return text.strip()


def scrape_rss(url):

    feed = feedparser.parse(url)
    news = []

    for entry in feed.entries:
        news.append({
            "title": entry.get("title", ""),
            "url": entry.get("link", ""),
            "content": clean_html(entry.get("summary", "")),
            "published_parsed": getattr(entry, "published_parsed", None),
        })

    return news