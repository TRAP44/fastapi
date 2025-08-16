from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import delete, update, asc, desc
from .models import Product, Order, OrderItem
from .connect import async_session


async def create_order(user_id: int, product_items: list[dict]):
    async with async_session() as session:
        order = Order(user_id=user_id)
        session.add(order)
        await session.flush()

        for item in product_items:
            session.add(OrderItem(
                order_id=order.id,
                product_id=item['product_id'],
                quantity=item.get('quantity', 1)
            ))

        await session.commit()
        await session.refresh(order)

        return order
    

async def get_order_by_id(order_id: int):
    async with async_session() as session:
        result = await session.execute(select(Order).where(Order.id == order_id).options(
            selectinload(Order.items).selectinload(OrderItem.product)
        ))
        return result.scalar_one_or_none()
    

async def get_all_order():
    async with async_session() as session:
        result = await session.execute(select(Order).options(selectinload(Order.items).selectinload(OrderItem.product)).order_by(Order.created_at.desc()))
        return result.scalars().all()
    

async def create_product(title: str, desc: str, price: float, image_url: str):
    async with async_session() as session:
        product = Product(title=title, desc=desc, price=price, image_url=image_url)
        session.add(product)
        await session.commit()
        await session.refresh(product)

        return product


async def get_all_product(order_by = "id", direction = "asc"):
    async with async_session() as session:
        column = getattr(Product, order_by, Product.id)
        direction_fn = asc if direction == "asc" else desc

        result = await session.execute(select(Product).order_by(direction_fn(column)))
        return result.scalars().all()


async def get_product_by_id(product_id: int):
    async with async_session() as session:
        result = await session.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()
    

async def get_product_by_title(title: str):
    async with async_session() as session:
        result = await session.execute(select(Product).where(Product.title.ilike(f"%{title}%")))
        return result.scalars().all()
    

async def update_order_status(order_id: int, status: str = "done"):
    async with async_session() as session:
        result = await session.excecute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()
        if order is None:
            return None
        
        order.status = status

        await session.commit()
        await session.refresh(order)

        return order