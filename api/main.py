from typing import List

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from services.property_service import property_service
from services.review_service import review_service
from services.comment_service import comment_service
from services.favorites_service import favorites_service
from domain.property import Property
from domain.review import Review
from domain.comment import Comment

app = FastAPI(title="CRUD EDD - Housing Reviews")

# Static files (CSS) y templates (HTML)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# =========================
# Pydantic Schemas (DTOs)
# =========================

class PropertyCreate(BaseModel):
    title: str
    country: str
    city: str


class PropertyUpdate(BaseModel):
    title: str
    country: str
    city: str


class ReviewCreate(BaseModel):
    title: str
    body: str
    rating: int


class ReviewUpdate(BaseModel):
    title: str
    body: str
    rating: int


class CommentCreate(BaseModel):
    body: str


class CommentUpdate(BaseModel):
    body: str


# =========================
# Helpers de serialización
# =========================

def serialize_property(prop: Property) -> dict:
    return {
        "id": prop.id,
        "title": prop.title,
        "country": prop.country,
        "city": prop.city,
    }


def serialize_review(review: Review) -> dict:
    return {
        "id": review.id,
        "property_id": review.property_id,
        "title": review.title,
        "body": review.body,
        "rating": review.rating,
    }


def serialize_comment(comment: Comment) -> dict:
    return {
        "id": comment.id,
        "review_id": comment.review_id,
        "body": comment.body,
    }


# =========================
# Rutas HTML sencillas
# =========================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    properties = property_service.list_properties()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "properties": properties},
    )


@app.get("/properties", response_class=HTMLResponse)
async def list_properties_view(request: Request):
    properties = property_service.list_properties()
    return templates.TemplateResponse(
        "properties.html",
        {"request": request, "properties": properties},
    )


# =========================
# API JSON - PROPERTIES
# =========================

@app.post("/api/properties", response_model=dict)
async def create_property(payload: PropertyCreate):
    prop = property_service.create_property(
        title=payload.title,
        country=payload.country,
        city=payload.city,
    )
    return serialize_property(prop)


@app.get("/api/properties", response_model=List[dict])
async def list_properties():
    props = property_service.list_properties()
    return [serialize_property(p) for p in props]


@app.get("/api/properties/{property_id}", response_model=dict)
async def get_property(property_id: int):
    prop = property_service.get_property(property_id)
    if prop is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return serialize_property(prop)


@app.put("/api/properties/{property_id}", response_model=dict)
async def update_property(property_id: int, payload: PropertyUpdate):
    prop = property_service.update_property(
        property_id, payload.title, payload.country, payload.city
    )
    if prop is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return serialize_property(prop)


@app.delete("/api/properties/{property_id}", response_model=dict)
async def delete_property(property_id: int):
    deleted = property_service.delete_property(property_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Property not found")
    return {"message": "Property deleted"}


# =========================
# API JSON - REVIEWS
# =========================

@app.post("/api/properties/{property_id}/reviews", response_model=dict)
async def create_review(property_id: int, payload: ReviewCreate):
    try:
        review = review_service.create_review(
            property_id, payload.title, payload.body, payload.rating
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Property not found")
    return serialize_review(review)


@app.get("/api/properties/{property_id}/reviews", response_model=List[dict])
async def list_reviews(property_id: int):
    reviews = review_service.list_reviews_by_property(property_id)
    return [serialize_review(r) for r in reviews]


@app.get("/api/reviews/{review_id}", response_model=dict)
async def get_review(review_id: int):
    review = review_service.get_review(review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return serialize_review(review)


@app.put("/api/reviews/{review_id}", response_model=dict)
async def update_review(review_id: int, payload: ReviewUpdate):
    review = review_service.update_review(
        review_id, payload.title, payload.body, payload.rating
    )
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return serialize_review(review)


@app.delete("/api/reviews/{review_id}", response_model=dict)
async def delete_review(review_id: int):
    deleted = review_service.delete_review(review_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"message": "Review deleted"}


# =========================
# API JSON - COMMENTS
# =========================

@app.post("/api/reviews/{review_id}/comments", response_model=dict)
async def create_comment(review_id: int, payload: CommentCreate):
    try:
        comment = comment_service.create_comment(review_id, payload.body)
    except ValueError:
        raise HTTPException(status_code=404, detail="Review not found")
    return serialize_comment(comment)


@app.get("/api/reviews/{review_id}/comments", response_model=List[dict])
async def list_comments(review_id: int):
    comments = comment_service.list_comments_by_review(review_id)
    return [serialize_comment(c) for c in comments]


@app.put("/api/comments/{comment_id}", response_model=dict)
async def update_comment(comment_id: int, payload: CommentUpdate):
    comment = comment_service.update_comment(comment_id, payload.body)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return serialize_comment(comment)


@app.delete("/api/comments/{comment_id}", response_model=dict)
async def delete_comment(comment_id: int):
    deleted = comment_service.delete_comment(comment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted"}


# =========================
# API JSON - FAVORITES
# =========================

@app.post("/api/favorites/{property_id}", response_model=dict)
async def add_favorite(property_id: int):
    try:
        favorites_service.add_favorite(property_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Property not found")
    return {"message": "Added to favorites"}


@app.get("/api/favorites", response_model=List[dict])
async def list_favorites():
    favorites = favorites_service.list_favorites()
    return [serialize_property(p) for p in favorites]


@app.delete("/api/favorites/{property_id}", response_model=dict)
async def remove_favorite(property_id: int):
    removed = favorites_service.remove_favorite(property_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return {"message": "Removed from favorites"}
