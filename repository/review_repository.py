from typing import List, Optional

from datastructures.SymbolTable import ST
from domain.review import Review
from domain.property import Property
from repository.property_repository import property_repository


class ReviewRepository:
    """
    Repositorio de reseñas.
    Guarda:
    - Tabla global de reseñas por id (ST)
    - Cada propiedad tiene su propia DoubleLinkedList de reseñas.
    """

    def __init__(self) -> None:
        self._table = ST()
        self._next_id = 1

    def create(self, property_obj: Property, title: str, body: str, rating: int) -> Review:
        review = Review(
            id=self._next_id,
            property_id=property_obj.id,
            title=title,
            body=body,
            rating=rating,
        )
        property_obj.add_review(review)
        self._table.put(self._next_id, review)
        self._next_id += 1
        return review

    def get(self, review_id: int) -> Optional[Review]:
        return self._table.get(review_id)

    def update(self, review_id: int, title: str, body: str, rating: int) -> Optional[Review]:
        review = self.get(review_id)
        if review is None:
            return None
        review.title = title
        review.body = body
        review.rating = rating
        self._table.put(review_id, review)
        return review

    def delete(self, review_id: int) -> bool:
        review = self.get(review_id)
        if review is None:
            return False

        prop = property_repository.get(review.property_id)
        if prop is not None:
            # Suponemos que DoubleLinkedList tiene remove
            prop.remove_review(review)

        self._table.delete(review_id)
        return True

    def list_by_property(self, property_id: int) -> List[Review]:
        prop = property_repository.get(property_id)
        if prop is None:
            return []
        return prop.get_reviews()


review_repository = ReviewRepository()
