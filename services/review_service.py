from typing import List, Optional

from domain.review import Review
from repository.review_repository import review_repository
from repository.property_repository import property_repository


class ReviewService:
    def create_review(self, property_id: int, title: str, body: str, rating: int) -> Review:
        prop = property_repository.get(property_id)
        if prop is None:
            raise ValueError("Property not found")
        return review_repository.create(prop, title, body, rating)

    def get_review(self, review_id: int) -> Optional[Review]:
        return review_repository.get(review_id)

    def update_review(self, review_id: int, title: str, body: str, rating: int) -> Optional[Review]:
        return review_repository.update(review_id, title, body, rating)

    def delete_review(self, review_id: int) -> bool:
        return review_repository.delete(review_id)

    def list_reviews_by_property(self, property_id: int) -> List[Review]:
        return review_repository.list_by_property(property_id)


review_service = ReviewService()
