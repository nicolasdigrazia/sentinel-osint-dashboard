from services.collectors.rss_collector import collect_rss_news
from services.collectors.signal_detector import detect_signals

def run():
    print("Recolectando noticias...")
    collect_rss_news()
    
  
    print("Done.")
