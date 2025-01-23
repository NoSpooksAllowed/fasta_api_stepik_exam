from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert, select, update
from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db_depends import get_db
from app.schemas import CreateProduct
from app.models.category import Category
from app.models.products import Product
from app.routers.auth import get_current_user

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/")
async def get_all_products(db: Annotated[AsyncSession, Depends(get_db)]):
    products = await db.scalars(select(Product).where(Product.is_active == True and Product.stock > 0))

    return products.all()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    create_product: CreateProduct,
    get_user: Annotated[dict, Depends(get_current_user)]
):
    if get_user.get("is_admin") or get_user.get("is_supplier"):
        await db.execute(insert(Product).values(
            name=create_product.name,
            slug=slugify(create_product.name),
            description=create_product.description,
            price=create_product.price,
            image_url=create_product.image_url,
            stock=create_product.stock,
            rating=0.0,
            category_id=create_product.category,
            supplier_id=get_user.get('id')
        ))

        await db.commit()

        return {
            "status_code": status.HTTP_201_CREATED,
            "transaction": "Succesful"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to use this method"
        )

@router.get("/{category_slug}")
async def product_by_category(db: Annotated[AsyncSession, Depends(get_db)], category_slug: str):
    main_category = await db.scalar(select(Category).where(Category.slug == category_slug))
    if main_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no category found"
        )

    subcategories = await db.scalars(select(Category).where(Category.parent_id == main_category.id))
    categories_and_subcategories = [main_category.id] + [i.id for i in subcategories.all()]
    products_category = await db.scalars(
        select(Product).where(Product.category_id.in_(categories_and_subcategories), Product.is_active == True,
                              Product.stock > 0))
    return products_category.all()


@router.get("/detail/{product_slug}")
async def product_detail(db: Annotated[AsyncSession, Depends(get_db)], product_slug: str):
    product = await db.scalar(select(Product).where(Product.slug == product_slug))  
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no product found"
        )

    return product

@router.put("/{product_slug}")
async def update_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    product_slug: str,
    update_product: CreateProduct,
    get_user: Annotated[dict, Depends(get_current_user)]
):
    product = await db.scalar(select(Product).where(Product.slug == product_slug))  
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no product found"
        )


    if get_user.get("is_admin") or get_user.get("is_supplier"):
        await db.execute(update(Product).where(Product.slug == product_slug).values(
            name=update_product.name,
            slug=slugify(update_product.name),
            description=update_product.description,
            price=update_product.price,
            image_url=update_product.image_url,
            stock=update_product.stock,
            rating=0.0 if update_product.rating is None else update_product.rating,
            category_id=update_product.category,
            supplier_id=get_user.get('id')
        ))    

        await db.commit()
        return {
            "status_code": status.HTTP_200_OK,
            "transaction": "Product update is succesful"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to use this method"
        )


@router.delete("/")
async def delete_product(
    db: Annotated[AsyncSession, Depends(get_db)],
    product_slug: str,
    get_user: Annotated[dict, Depends(get_current_user)]
):
    product = await db.scalar(select(Product).where(Product.slug == product_slug))  
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no product found"
        )

    if get_user.get("is_admin") or get_user.get("is_supplier"):
        await db.execute(update(Product).where(Product.slug == product_slug).values(is_active=False))
        await db.commit()

        return {
            "status_code": status.HTTP_200_OK,
            "transaction": "Product delete is successful"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to use this method"
        )
