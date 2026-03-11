from django.db import models


class Source(models.Model):

    SOURCE_TYPES = [
        ("news", "News"),
        ("twitter", "Twitter"),
        ("reddit", "Reddit"),
        ("website", "Website"),
        ("telegram", "Telegram"),
    ]

    CATEGORIES = [
        ("energia", "Energía"),
        ("financiero", "Financiero"),
        ("regulatorio", "Regulatorio"),
        ("politica", "Política"),
        ("economia", "Economía"),
        ("mundo", "Mundo / Internacional"),
        ("consumo_masivo", "Consumo Masivo"),
        ("general", "General"),
    ]

    name = models.CharField(max_length=200)
    url = models.URLField()
    source_type = models.CharField(max_length=50, choices=SOURCE_TYPES)
    category = models.CharField(max_length=50, choices=CATEGORIES, default="general")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class RawData(models.Model):

    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    content = models.TextField()
    url = models.URLField(unique=True)
    published_at = models.DateTimeField(null=True, blank=True)
    collected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class IntelligenceReport(models.Model):

    CATEGORIES = [
        ("energia", "Energía"),
        ("financiero", "Financiero"),
        ("regulatorio", "Regulatorio"),
        ("consumo_masivo", "Consumo Masivo"),
        ("reputacional", "Reputacional"),
        ("general", "General"),
    ]

    raw_data = models.ForeignKey(RawData, on_delete=models.CASCADE)
    summary = models.TextField()
    confidence_score = models.FloatField(default=0.5)
    analyst_notes = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORIES, default="general")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report {self.id} - {self.category}"