from dataclasses import dataclass


@dataclass
class MentionDTO:
    text: str    # "YPF"
    label: str   # "ORG"
    count: int   # cuántas veces aparece en la noticia
    context: str # oración donde aparece