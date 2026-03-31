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
    category = models.CharField(max_length=50, default="general")
    published_at = models.DateTimeField(null=True, blank=True)
    collected_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

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


        
        
        
class Entity(models.Model):

    ENTITY_TYPES = [
        ("PER", "Persona"),
        ("ORG", "Organización"),
        ("LOC", "Lugar"),
        ("MISC", "Miscelánea"),
        ("DATE", "Fecha"),
        ("MONEY", "Dinero/Cantidad"),
    ]

    name = models.CharField(max_length=200)                              
    normalized_name = models.CharField(max_length=200, blank=True, db_index=True)  # con índice para búsquedas rápidas
    label = models.CharField(max_length=10, choices=ENTITY_TYPES)
    aliases = models.JSONField(default=list, blank=True)
    description = models.TextField(blank=True)
    sector = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    news_appearance_count = models.IntegerField(default=0)
    last_seen = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "entities"
        ordering = ["-news_appearance_count", "-last_seen"]
        unique_together = ("normalized_name", "label")  # evita duplicados como "YPF" (ORG) y "YPF" (PER) siendo lo mismo

    def __str__(self):
        return f"{self.name} ({self.label})"


class EntityMention(models.Model):

    SENTIMENT_CHOICES = [
        ("positive", "Positivo"),
        ("negative", "Negativo"),
        ("neutral", "Neutral"),
    ]

    POSITION_CHOICES = [
        ("title", "Título"),
        ("body", "Cuerpo"),
        ("both", "Ambos"),
    ]

    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="mentions")
    raw_data = models.ForeignKey(RawData, on_delete=models.CASCADE, related_name="entity_mentions")
    count = models.IntegerField(default=1)
    context = models.TextField(blank=True)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, default="body")
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES, null=True, blank=True)
    relevance_score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("entity", "raw_data")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.entity.name} en '{self.raw_data.title[:50]}'"
