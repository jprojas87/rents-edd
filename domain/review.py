from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from datastructures.LinkedQueue import LinkedQueue  # Ajusta si tu nombre de clase cambia


@dataclass
class Review:
    id: int
    property_id: int
    title: str
    body: str
    rating: int
    comments: LinkedQueue = field(default_factory=LinkedQueue)

    def add_comment(self, comment: "Comment") -> None:
        """Agrega un comentario a la cola de comentarios."""
        # Suponemos que LinkedQueue tiene enqueue.
        self.comments.enqueue(comment)

    def get_comments(self) -> List["Comment"]:
        """Devuelve una lista con todos los comentarios."""
        return [comment for comment in self.comments]
