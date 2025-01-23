from pydantic import BaseModel, Field

class CreateProduct(BaseModel):
    name: str
    description: str
    price: int
    image_url: str
    stock: int
    category: int
    rating: float | None = None


class CreateCategory(BaseModel):
    name: str
    parent_id: int | None = None


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str

class CreateRating(BaseModel):
    grade: float = Field(..., ge=0.0, le=10.0)

class CreateReview(BaseModel):
    comment: str

class CreateRatingAndReview(CreateRating, CreateReview):
    pass
