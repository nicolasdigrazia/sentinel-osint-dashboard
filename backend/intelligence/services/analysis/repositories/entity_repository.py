import unicodedata
from typing import List

from django.utils import timezone

from intelligence.models import Entity, EntityMention, RawData
from ..dto import MentionDTO


class EntityRepository:

    def save_mentions(self, raw_data: RawData, mentions: List[MentionDTO]) -> None:
        for mention in mentions:
            entity = self._get_or_create_entity(mention)
            self._save_mention_individual(entity, raw_data, mention)
            self._update_entity_stats(entity)

    def _get_or_create_entity(self, mention: MentionDTO) -> Entity:
        normalized = self._normalize(mention.text)

        entity, created = Entity.objects.get_or_create(
            normalized_name=normalized,
            label=mention.label,
            defaults={"name": mention.text}
        )

        return entity

    def _save_mention_individual(self, entity: Entity, raw_data: RawData, mention: MentionDTO) -> None:
        # update_or_create: si ya existe el par (entity + raw_data) lo actualiza,
        # si no existe lo crea. Esto evita duplicados.
        EntityMention.objects.update_or_create(
            entity=entity,
            raw_data=raw_data,
            defaults={
                "count": mention.count,
                "context": mention.context,
            }
        )

    def _update_entity_stats(self, entity: Entity) -> None:
        # Actualizamos el conteo total de menciones y la última vez que se vio la entidad
        entity.news_appearance_count = entity.mentions.count()
        entity.last_seen = timezone.now()
        entity.save(update_fields=["news_appearance_count", "last_seen"])

    def _normalize(self, text: str) -> str:
        text = text.strip().lower()
        return "".join(
            c for c in unicodedata.normalize("NFD", text)
            if unicodedata.category(c) != "Mn"
        )