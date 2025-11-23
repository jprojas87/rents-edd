from typing import List, Optional

from domain.comment import Comment
from repository.comment_repository import comment_repository
from repository.review_repository import review_repository


class CommentService:
    def create_comment(self, review_id: int, body: str) -> Comment:
        review = review_repository.get(review_id)
        if review is None:
            raise ValueError("Review not found")
        return comment_repository.create(review, body)

    def get_comment(self, comment_id: int) -> Optional[Comment]:
        return comment_repository.get(comment_id)

    def update_comment(self, comment_id: int, body: str) -> Optional[Comment]:
        return comment_repository.update(comment_id, body)

    def delete_comment(self, comment_id: int) -> bool:
        return comment_repository.delete(comment_id)

    def list_comments_by_review(self, review_id: int) -> List[Comment]:
        return comment_repository.list_by_review(review_id)


comment_service = CommentService()
