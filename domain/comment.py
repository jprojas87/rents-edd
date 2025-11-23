from dataclasses import dataclass


@dataclass
class Comment:
    id: int
    review_id: int
    body: str
