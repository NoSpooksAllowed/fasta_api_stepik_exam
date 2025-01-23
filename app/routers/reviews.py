from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db_depends import get_db
from app.schemas import CreateRatingAndReview
from app.routers.auth import get_current_user
from app.models.rating import Rating
from app.models.products import Product
import app.utils.reviews

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.get("/")
async def all_reviews(db: Annotated[AsyncSession, Depends((get_db))]):
    query = app.utils.reviews.get_all_reviews_query() 

    result = await db.execute(query)
    rows = result.all()

    merged_entities = [
        {
            "rating_id": row.rating_id,
            "grade": row.grade,
            "review_id": row.review_id,
            "comment": row.comment,
            "comment_date": row.comment_date,
        }
        for row in rows
    ]

    return merged_entities


@router.get("/{product_slug}")
async def products_reviews(db: Annotated[AsyncSession, Depends(get_db)], product_slug: str):
    product = await db.scalar(select(Product).where(Product.slug == product_slug))  

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no product found"
        )

    query = app.utils.reviews.get_reviews_query_by_product_id(product.id) 
    result = await db.execute(query)
    rows = result.all()

    merged_entities = [
        {
            "rating_id": row.rating_id,
            "grade": row.grade,
            "review_id": row.review_id,
            "comment": row.comment,
            "comment_date": row.comment_date,
        }
        for row in rows
    ]

    return merged_entities

@router.post("/{product_slug}")
async def add_review(
    db: Annotated[AsyncSession, Depends(get_db)],
    get_user: Annotated[dict, Depends(get_current_user)],
    product_slug: str,
    rating_and_review: CreateRatingAndReview
):
    product = await db.scalar(select(Product).where(Product.slug == product_slug))

    if product == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This product doesn't exist"
        )

    if get_user.get("is_customer"):
        result = await app.utils.reviews.save_review(db, get_user.get("id"), product.id, rating_and_review.comment)   

        await app.utils.reviews.save_rating(db, get_user.get("id"), product.id, rating_and_review.grade, result.inserted_primary_key[0])

        ratings = await db.execute(select(Rating.grade).where(Rating.product_id == product.id))
        all_ratings = ratings.scalars().all()

        if all_ratings:
            mean_rating = sum(all_ratings) / len(all_ratings)
            product.rating = mean_rating
            db.add(product)
            await db.commit()

        return {
            "status_code": status.HTTP_201_CREATED,
            "transaction": "Succesful"
        }


    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customer can use this method"
        )


@router.delete("/{product_slug}")
async def delete_reviews(
    db: Annotated[AsyncSession, Depends(get_db)],
    get_user: Annotated[dict, Depends(get_current_user)],
    product_slug: str,
    review_id: int
):
    product = await db.scalar(select(Product).where(Product.slug == product_slug))

    if product == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This product doesn't exist"
        )

    if get_user.get("is_admin"):
        await app.utils.reviews.delete_review_query(db, product.id, review_id)

        return {
            "status_code": status.HTTP_200_OK,
            "transaction": "Review delete is successful"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can use this method"
        )
