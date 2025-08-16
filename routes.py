from fastapi import APIRouter, Response, Request
from pydantic import BaseModel, Field
from typing import List
from db.crud import (
    create_product,
    get_all_product,
    get_product_by_id,
    get_product_by_title,
    create_order,
    get_all_order,
    get_order_by_id,
    update_order_status
)

router = APIRouter()


class ProductModel(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    desc: str = Field(..., min_length=5)
    price: float = Field(..., gt=0)
    image_url: str


class OrderItemModel(BaseModel):
    product_id: int
    quantity: int = Field(default=1, gt=0)


class OrderCreateModel(BaseModel):
    user_id: int
    items: List[OrderItemModel] 


@router.post("/product/add")
async def product_add(data: ProductModel):
    return await create_product(data.title, data.desc, data.price, data.image_url)


@router.get("/products")
async def get_product(order_by, direction):
    return await get_all_product(order_by, direction)


@router.get("/product/{product_id}")
async def get_product(product_id: int):
    return await get_product_by_id(product_id)


@router.get("/product/search/{title}")
async def get_product_title(title: str):
    return await get_product_by_title(title)


@router.get("/orders")
async def get_orders():
    return await get_all_order()


@router.get("/orders/{orders_id}")
async def get_orders(orders_id: int):
    return await get_order_by_id(orders_id)


@router.post("/order/add")
async def order_add(data: OrderCreateModel):
    return await create_order(data.user_id, [item.model_dump() for item in data.items])


@router.post("/webhook/fondy")
async def fondy_callback(request):
    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type:
        data = await request.json()
    elif "application/x-www-form-urlencoded" in content_type:
        form_data = await request.form()
        data = dict(form_data)
    else:
        return Response(status_code=400, content="Unsupported content type")
    

    foundy_order_id = data.get("order_id")
    order_id = int(foundy_order_id.split("_")[1])

    if data.get("order_status") == "approved":
        await update_order_status(order_id, "done")
    else:
        await update_order_status(order_id, "fail")