from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.rating import Rating
from app.models.review import Review



def get_all_reviews_query():
    return (
        select(
            Rating.id.label("rating_id"),
            Rating.grade.label("grade"),
            Review.id.label("review_id"),
            Review.comment.label("comment"),
            Review.comment_date.label("comment_date")
        )
        .join(Review, Rating.review_id == Review.id)
        .where(
            Rating.is_active == True,         
            Review.is_active == True                  
        )
    )

def get_reviews_query_by_product_id(product_id: int):
    return (
        select(
            Rating.id.label("rating_id"),
            Rating.grade.label("grade"),
            Review.id.label("review_id"),
            Review.comment.label("comment"),
            Review.comment_date.label("comment_date")
        )
        .join(Review, Rating.review_id == Review.id)
        .where(
            Rating.is_active == True,         
            Review.is_active == True,
            Rating.product_id == product_id,
            Review.product_id == product_id
        )
    )


async def save_review(db: AsyncSession, user_id: int, product_id: int, comment: str):
    result = await db.execute(insert(Review).values(
        user_id=user_id,
        product_id=product_id,
        comment=comment
    ))

    await db.commit()

    return result

async def save_rating(db: AsyncSession, user_id: int, product_id:int, grade: float, review_id: int):
    await db.execute(insert(Rating).values(
        user_id=user_id,
        product_id=product_id,
        grade=grade,
        review_id=review_id,
    ))

    await db.commit()


async def delete_review_query(db: AsyncSession, product_id: int, review_id: int):
    await db.execute(
        update(Review)
        .where(
            Review.product_id == product_id,
            Review.id == review_id
        )
        .values(is_active=False)
    ) 

    await db.execute(
        update(Rating)
        .where(
            Rating.product_id == product_id,
            Rating.review_id == review_id
        )
        .values(is_active=False)
    )

    await db.commit()


