from django.contrib import admin
from .models import Source, RawData, IntelligenceReport

class RawDataAdmin(admin.ModelAdmin):
    list_display = ["title", "get_category", "published_at", "collected_at", "source"]
    list_filter = ["source__category", "source__name"]
    ordering = ["-published_at", "-collected_at"]  

    def get_category(self, obj):
        return obj.source.category
    get_category.short_description = "Categoría"

admin.site.register(Source)
admin.site.register(RawData, RawDataAdmin)
admin.site.register(IntelligenceReport)