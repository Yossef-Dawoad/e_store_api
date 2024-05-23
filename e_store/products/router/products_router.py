from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from e_store.db import get_session
from e_store.products.models.products import Product, ProductCreate, ProductPublic
from e_store.products.services import create_new_product, verify_category_exists

router = APIRouter(tags=["Products"], prefix="/products")


@router.post("/", response_model=ProductPublic, status_code=201)
async def create_product(  # noqa: ANN201
    *,
    session: Annotated[AsyncSession, Depends(get_session)],
    product: ProductCreate,
):
    category_exists = verify_category_exists(product.category_id, session)
    if not category_exists:
        raise HTTPException(
            status_code=400,
            detail="You Provided Invalid categroy id",
        )
    db_product = await create_new_product(product, session)
    return db_product


@router.get("/", response_model=list[ProductPublic])
async def read_products(  # noqa: ANN201
    *,
    session: Annotated[AsyncSession, Depends(get_session)],
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    stmt = select(Product).offset(offset).limit(limit)
    products = (await session.exec(stmt)).all()
    return products
