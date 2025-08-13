from fastapi import APIRouter
from pydantic import BaseModel, Field, EmailStr
from db.crud import create_user, get_all_users, get_user_by_id, update_user, delete_user

router = APIRouter()


class UserModel(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    #age: int = Field(..., ge=10, le=100)
    #city: str | None = None


@router.post("/reg")
async def reg(data: UserModel):
    return await create_user(data.name, data.email)


@router.get("/users")
async def get_user(order_by, direction):
    return await get_all_users(order_by, direction)


@router.get("/users/{user_id}")
async def get_user(user_id: int):
    return await get_user_by_id(user_id)


@router.put("/users/{user_id}")
async def update_user_data(user_id: int, data: UserModel):
    return await update_user(user_id, data.name, data.email)


@router.delete("/users/{user_id}")
async def delete_user_data(user_id: int):
    return await delete_user(user_id)