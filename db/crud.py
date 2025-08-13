from sqlalchemy.future import select
from sqlalchemy import delete, update, asc, desc
from .models import User
from .connect import async_session


async def create_user(name: str, email: str):
    async with async_session() as session:
        user = User(name=name, email=email)
        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user


async def get_all_users(order_by = "id", direction = "asc"):
    async with async_session() as session:
        column = getattr(User, order_by, User.id)
        direction_fn = asc if direction == "asc" else desc

        result = await session.execute(select(User).order_by(direction_fn(column)))
        return result.scalars().all()


async def get_user_by_id(user_id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    

async def update_user(user_id: int, name: str, email: str):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            return None
        
        user.name = name
        user.email = email
        await session.commit()
        await session.refresh(user)

        return user
    

async def delete_user(user_id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            return None
        
        await session.delete(user)
        await session.commit()

        return True