from django.contrib import admin
from .models import Source, RawData, IntelligenceReport

admin.site.register(Source)
admin.site.register(RawData)
admin.site.register(IntelligenceReport)