from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from e_store.db import get_session
from e_store.orders.models import OrderPublic
from e_store.orders.services import create_new_order, get_list_of_order

router = APIRouter(tags=["Orders"], prefix="/orders")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderPublic)
async def initiate_order(  # noqa: ANN201
    *,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    return await create_new_order(session)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[OrderPublic])
async def read_orders(  # noqa: ANN201
    *,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    return await get_list_of_order(session)
