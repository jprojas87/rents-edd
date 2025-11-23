from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from datastructures.DoubleLinkedList import DoubleLinkedList  # Ajusta si tu nombre de clase cambia


@dataclass
class Property:
    id: int
    title: str
    country: str
    city: str
    reviews: DoubleLinkedList = field(default_factory=DoubleLinkedList)

    def add_review(self, review: "Review") -> None:
        """Agrega una reseña a la lista de reseñas de la propiedad."""
        # Suponemos que DoubleLinkedList tiene un método append.
        self.reviews.append(review)

    def remove_review(self, review: "Review") -> None:
        """Elimina una reseña de la lista de reseñas."""
        # Suponemos que DoubleLinkedList tiene un método remove.
        self.reviews.remove(review)

    def get_reviews(self) -> List["Review"]:
        """Devuelve una lista normal de reseñas (para serializar)."""
        # Suponemos que DoubleLinkedList es iterable.
        return [review for review in self.reviews]
