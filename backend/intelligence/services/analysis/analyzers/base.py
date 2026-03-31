from abc import ABC, abstractmethod
from typing import List
from ..dto import MentionDTO


class BaseAnalyzer(ABC):
    """
    Interfaz que todo analyzer debe cumplir.
    NLPPipeline depende de esto, no de spaCy directamente.
    """

    @abstractmethod
    def extract(self, title: str, body: str) -> List[MentionDTO]:
        """
        Recibe el texto de una noticia y devuelve las entidades encontradas.
        """
        raise NotImplementedError