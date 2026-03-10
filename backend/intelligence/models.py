from django.db import models


class Source(models.Model):

    SOURCE_TYPES = [
        ("news", "News"),
        ("twitter", "Twitter"),
        ("reddit", "Reddit"),
        ("website", "Website"),
        ("telegram", "Telegram"),
    ]

    name = models.CharField(max_length=200)
    url = models.URLField()
    source_type = models.CharField(max_length=50, choices=SOURCE_TYPES)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class RawData(models.Model):

    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    title = models.CharField(max_length=500)
    content = models.TextField()

    collected_at = models.DateTimeField(auto_now_add=True)

    url = models.URLField(unique=True)

    def __str__(self):
        return self.title


class IntelligenceReport(models.Model):

    raw_data = models.ForeignKey(RawData, on_delete=models.CASCADE)

    summary = models.TextField()

    confidence_score = models.FloatField(default=0.5)

    analyst_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report {self.id}"