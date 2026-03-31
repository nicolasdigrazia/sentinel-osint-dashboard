import unicodedata
from typing import List

import spacy
from spacy.language import Language

from ..dto import MentionDTO
from .base import BaseAnalyzer


LABELS_TO_IGNORE = {"DATE", "TIME", "PERCENT", "CARDINAL", "ORDINAL"}


class SpacyAnalyzer(BaseAnalyzer):

    _instance = None  # singleton para no recargar el modelo cada vez

    def __init__(self, model_name: str = "es_core_news_lg"):
        self._model_name = model_name
        self._nlp = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load_model(self):
        if self._nlp is None:
            self._nlp = spacy.load(self._model_name)
        return self._nlp

    def extract(self, title: str, body: str) -> List[MentionDTO]:
        nlp = self._load_model()

        # Procesamos título y cuerpo juntos, separados por punto
        # para que spaCy los trate como un solo documento
        full_text = f"{title}. {body}"
        doc = nlp(full_text)

        # Contamos cuántas veces aparece cada entidad
        # key: (texto_normalizado, label) → para agrupar "YPF" y "ypf" como lo mismo
        entity_counts = {}

        for ent in doc.ents:
            if ent.label_ in LABELS_TO_IGNORE:
                continue
            if len(ent.text.strip()) < 2:
                continue

            key = (self._normalize(ent.text), ent.label_)

            if key not in entity_counts:
                entity_counts[key] = {
                    "original": ent.text,
                    "count": 0,
                    "context": self._get_context(doc, ent),
                }

            entity_counts[key]["count"] += 1

        # Convertimos a lista de DTOs
        mentions = []
        for (normalized, label), data in entity_counts.items():
            mentions.append(MentionDTO(
                text=data["original"],
                label=label,
                count=data["count"],
                context=data["context"],
            ))

        return mentions

    def _get_context(self, doc, ent) -> str:
        """Devuelve la oración donde aparece la entidad."""
        for sent in doc.sents:
            if ent.start >= sent.start and ent.end <= sent.end:
                return sent.text.strip()
        return ent.text

    def _normalize(self, text: str) -> str:
        """Lowercase sin tildes: 'Milei' y 'milei' → 'milei'"""
        text = text.strip().lower()
        return "".join(
            c for c in unicodedata.normalize("NFD", text)
            if unicodedata.category(c) != "Mn"
        )