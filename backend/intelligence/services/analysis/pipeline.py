import logging
from typing import List

from django.db.models import QuerySet

from intelligence.models import RawData
from .analyzers.base import BaseAnalyzer
from .analyzers.spacy_analyzer import SpacyAnalyzer
from .repositories.entity_repository import EntityRepository

logger = logging.getLogger(__name__)


class NLPPipeline:

    def __init__(self, analyzer=None, repository=None):
        self.analyzer = analyzer or SpacyAnalyzer.get_instance()
        self.repository = repository or EntityRepository()

    def analyze(self, raw_data: RawData) -> None:
        try:
            mentions = self.analyzer.extract(
                title=raw_data.title,
                body=raw_data.content,
            )
            self.repository.save_mentions(raw_data, mentions)
            logger.info(f"[NLPPipeline] {len(mentions)} entidades en: {raw_data.title[:60]}")
        except Exception as e:
            logger.error(f"[NLPPipeline] Error en RawData #{raw_data.id}: {e}")