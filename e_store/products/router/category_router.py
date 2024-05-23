from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from e_store.db import get_session
from e_store.products.models import Category, CategoryPublic
from e_store.products.services import create_new_category

router = APIRouter(tags=["Products"], prefix="/products")


@router.post("/category", response_model=Category, status_code=201)
async def create_category(  # noqa: ANN201
    *,
    session: Annotated[AsyncSession, Depends(get_session)],
    category: Category,
):
    db_category = await create_new_category(category, session)
    return db_category


@router.get("/category", response_model=list[CategoryPublic])
async def read_categories(  # noqa: ANN201
    *,
    session: Annotated[AsyncSession, Depends(get_session)],
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    stmt = select(Category).offset(offset).limit(limit)
    categories = (await session.exec(stmt)).all()
    return categories


@router.get("/category/{category_id}", response_model=CategoryPublic)
async def read_category(  # noqa: ANN201
    *,
    session: Annotated[AsyncSession, Depends(get_session)],
    category_id: int,
):
    if not (category := await session.get(Category, category_id)):
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.delete("/category/{category_id}", status_code=204)
async def delete_category(  # noqa: ANN201
    *,
    session: Annotated[AsyncSession, Depends(get_session)],
    category_id: int,
):
    if not (category := await session.get(Category, category_id)):
        raise HTTPException(status_code=404, detail="Category not found")
    await session.delete(category)
    await session.commit()
    return {"ok": True}
