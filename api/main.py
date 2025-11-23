from typing import List

from fastapi import FastAPI, HTTPException, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
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

app = FastAPI(title="RentView - Housing Reviews")

# Static files (CSS) y templates (HTML)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# =========================
# Pydantic Schemas (DTOs)
# =========================

class PropertyCreate(BaseModel):
    address: str
    body: str
    rating: int


class PropertyUpdate(BaseModel):
    address: str
    body: str
    rating: int


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
        "address": prop.address,
        "body": prop.body,
        "rating": prop.rating,
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


@app.get("/properties/new", response_class=HTMLResponse)
async def new_property_form(request: Request):
    return templates.TemplateResponse(
        "property_form.html",
        {
            "request": request,
            "form_action": "/properties/new",
            "form_method": "post",
            "address": "",
            "body": "",
            "rating": 4,
            "heading": "Crear propiedad",
            "submit_label": "Crear",
        },
    )


@app.post("/properties/new")
async def create_property_html(
    address: str = Form(...),
    body: str = Form(...),
    rating: int = Form(...),
):
    prop = property_service.create_property(address, body, rating)
    return RedirectResponse(
        url=f"/properties/{prop.id}", status_code=status.HTTP_303_SEE_OTHER
    )


@app.get("/properties/{property_id}", response_class=HTMLResponse)
async def property_detail(request: Request, property_id: int):
    prop = property_service.get_property(property_id)
    if prop is None:
        raise HTTPException(status_code=404, detail="Property not found")
    reviews = review_service.list_reviews_by_property(property_id)
    favorites = favorites_service.list_favorites()
    is_favorite = any(fav.id == prop.id for fav in favorites)
    return templates.TemplateResponse(
        "property_detail.html",
        {
            "request": request,
            "property": prop,
            "reviews": reviews,
            "is_favorite": is_favorite,
        },
    )


@app.get("/properties/{property_id}/edit", response_class=HTMLResponse)
async def edit_property_form(request: Request, property_id: int):
    prop = property_service.get_property(property_id)
    if prop is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return templates.TemplateResponse(
        "property_form.html",
        {
            "request": request,
            "form_action": f"/properties/{property_id}/edit",
            "form_method": "post",
            "address": prop.address,
            "body": prop.body,
            "rating": prop.rating,
            "heading": "Editar propiedad",
            "submit_label": "Actualizar",
        },
    )


@app.post("/properties/{property_id}/edit")
async def update_property_html(
    property_id: int,
    address: str = Form(...),
    body: str = Form(...),
    rating: int = Form(...),
):
    prop = property_service.update_property(property_id, address, body, rating)
    if prop is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return RedirectResponse(
        url=f"/properties/{property_id}", status_code=status.HTTP_303_SEE_OTHER
    )


@app.post("/properties/{property_id}/delete")
async def delete_property_html(property_id: int):
    property_service.delete_property(property_id)
    return RedirectResponse(url="/properties", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/properties/{property_id}/reviews/new")
async def create_review_html(
    property_id: int,
    title: str = Form(...),
    body: str = Form(...),
    rating: int = Form(...),
):
    try:
        review_service.create_review(property_id, title, body, rating)
    except ValueError:
        raise HTTPException(status_code=404, detail="Property not found")
    return RedirectResponse(
        url=f"/properties/{property_id}", status_code=status.HTTP_303_SEE_OTHER
    )


@app.get("/reviews/{review_id}", response_class=HTMLResponse)
async def review_detail(request: Request, review_id: int):
    review = review_service.get_review(review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    prop = property_service.get_property(review.property_id)
    comments = comment_service.list_comments_by_review(review_id)
    return templates.TemplateResponse(
        "review_detail.html",
        {
            "request": request,
            "review": review,
            "property": prop,
            "comments": comments,
        },
    )


@app.get("/reviews/{review_id}/edit", response_class=HTMLResponse)
async def edit_review_form(request: Request, review_id: int):
    review = review_service.get_review(review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return templates.TemplateResponse(
        "review_form.html",
        {
            "request": request,
            "review": review,
            "form_action": f"/reviews/{review_id}/edit",
            "form_method": "post",
            "heading": "Editar reseña",
            "submit_label": "Actualizar",
        },
    )


@app.post("/reviews/{review_id}/edit")
async def update_review_html(
    review_id: int,
    title: str = Form(...),
    body: str = Form(...),
    rating: int = Form(...),
):
    review = review_service.update_review(review_id, title, body, rating)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return RedirectResponse(
        url=f"/reviews/{review_id}", status_code=status.HTTP_303_SEE_OTHER
    )


@app.post("/reviews/{review_id}/delete")
async def delete_review_html(review_id: int):
    review = review_service.get_review(review_id)
    property_id = review.property_id if review else None
    review_service.delete_review(review_id)
    redirect_url = (
        f"/properties/{property_id}" if property_id is not None else "/properties"
    )
    return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)


@app.post("/reviews/{review_id}/comments/new")
async def create_comment_html(review_id: int, body: str = Form(...)):
    try:
        comment_service.create_comment(review_id, body)
    except ValueError:
        raise HTTPException(status_code=404, detail="Review not found")
    return RedirectResponse(
        url=f"/reviews/{review_id}", status_code=status.HTTP_303_SEE_OTHER
    )


@app.get("/comments/{comment_id}/edit", response_class=HTMLResponse)
async def edit_comment_form(request: Request, comment_id: int):
    comment = comment_service.get_comment(comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return templates.TemplateResponse(
        "comment_form.html",
        {
            "request": request,
            "comment": comment,
            "form_action": f"/comments/{comment_id}/edit",
            "form_method": "post",
            "heading": "Editar comentario",
            "submit_label": "Actualizar",
        },
    )


@app.post("/comments/{comment_id}/edit")
async def update_comment_html(comment_id: int, body: str = Form(...)):
    comment = comment_service.update_comment(comment_id, body)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    review_id = comment.review_id
    return RedirectResponse(
        url=f"/reviews/{review_id}", status_code=status.HTTP_303_SEE_OTHER
    )


@app.post("/comments/{comment_id}/delete")
async def delete_comment_html(comment_id: int):
    comment = comment_service.get_comment(comment_id)
    review_id = comment.review_id if comment else None
    comment_service.delete_comment(comment_id)
    redirect_url = f"/reviews/{review_id}" if review_id is not None else "/properties"
    return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)


@app.post("/favorites/{property_id}")
async def add_favorite_html(property_id: int):
    try:
        favorites_service.add_favorite(property_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Property not found")
    return RedirectResponse(
        url=f"/properties/{property_id}", status_code=status.HTTP_303_SEE_OTHER
    )


@app.get("/favorites", response_class=HTMLResponse)
async def list_favorites_view(request: Request):
    favorites = favorites_service.list_favorites()
    return templates.TemplateResponse(
        "favorites.html",
        {"request": request, "favorites": favorites},
    )


@app.post("/favorites/{property_id}/delete")
async def remove_favorite_html(property_id: int):
    favorites_service.remove_favorite(property_id)
    return RedirectResponse(url="/favorites", status_code=status.HTTP_303_SEE_OTHER)


# =========================
# API JSON - PROPERTIES
# =========================

@app.post("/api/properties", response_model=dict)
async def create_property(payload: PropertyCreate):
    prop = property_service.create_property(
        address=payload.address,
        body=payload.body,
        rating=payload.rating,
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
        property_id, payload.address, payload.body, payload.rating
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
