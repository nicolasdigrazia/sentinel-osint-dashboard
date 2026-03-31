from django.contrib import admin
from .models import Source, RawData, IntelligenceReport, Entity, EntityMention

class RawDataAdmin(admin.ModelAdmin):
    list_display = ["title", "get_category", "published_at", "collected_at", "source"]
    list_filter = ["source__category", "source__name"]
    ordering = ["-published_at", "-collected_at"]  

    def get_category(self, obj):
        return obj.source.category
    get_category.short_description = "Categoría"

@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ["name", "label", "news_appearance_count", "last_seen"]
    list_filter = ["label"]
    search_fields = ["name", "normalized_name"]
    ordering = ["-news_appearance_count"]


@admin.register(EntityMention)
class EntityMentionAdmin(admin.ModelAdmin):
    list_display = ["entity", "raw_data", "count", "created_at"]
    list_filter = ["entity__label"]
    search_fields = ["entity__name", "raw_data__title"]
    ordering = ["-created_at"]

admin.site.register(Source)
admin.site.register(RawData, RawDataAdmin)
admin.site.register(IntelligenceReport)