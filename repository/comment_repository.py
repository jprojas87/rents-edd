from typing import List, Optional

from datastructures.SymbolTable import ST
from datastructures.LinkedQueue import LinkedQueue
from domain.comment import Comment
from domain.review import Review
from repository.review_repository import review_repository


class CommentRepository:
    """
    Repositorio de comentarios.

    - Tabla global de comentarios por id (ST)
    - Cada reseña guarda sus comentarios en una LinkedQueue.
    """

    def __init__(self) -> None:
        self._table = ST()
        self._next_id = 1

    def create(self, review: Review, body: str) -> Comment:
        comment = Comment(id=self._next_id, review_id=review.id, body=body)
        review.add_comment(comment)
        self._table.put(self._next_id, comment)
        self._next_id += 1
        return comment

    def get(self, comment_id: int) -> Optional[Comment]:
        return self._table.get(comment_id)

    def update(self, comment_id: int, body: str) -> Optional[Comment]:
        comment = self.get(comment_id)
        if comment is None:
            return None
        comment.body = body
        self._table.put(comment_id, comment)
        return comment

    def delete(self, comment_id: int) -> bool:
        comment = self.get(comment_id)
        if comment is None:
            return False

        review = review_repository.get(comment.review_id)
        if review is not None:
            # Reconstruimos la cola excluyendo el comentario a eliminar.
            old_queue = review.comments
            new_queue = LinkedQueue()
            for c in old_queue:
                if c.id != comment_id:
                    new_queue.enqueue(c)
            review.comments = new_queue

        self._table.delete(comment_id)
        return True

    def list_by_review(self, review_id: int) -> List[Comment]:
        review = review_repository.get(review_id)
        if review is None:
            return []
        return review.get_comments()


comment_repository = CommentRepository()
