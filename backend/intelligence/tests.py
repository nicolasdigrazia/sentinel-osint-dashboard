from django.test import TestCase
from django.db import IntegrityError
from .models import Source, RawData

class SourceModelTest(TestCase):
    def test_create_source(self):
        source = Source.objects.create(
            name="Test Source",
            url="https://example.com/rss",
            source_type="news"
        )
        self.assertEqual(source.name, "Test Source")

class RawDataModelTest(TestCase):
    def test_unique_url(self):
        RawData.objects.create(
            title="Noticia",
            url="https://example.com/news",
            source=Source.objects.create(
                name="Fuente",
                url="https://fuente.com",
                source_type="news"
            )
        )
        with self.assertRaises(IntegrityError):
            RawData.objects.create(
                title="Duplicada",
                url="https://example.com/news",
                source=Source.objects.get(name="Fuente")
            )