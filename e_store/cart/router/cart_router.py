from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from e_store.cart.models import CartItem, CartPublic
from e_store.cart.services import add_to_cart, get_all_cart_items
from e_store.db import get_session

router = APIRouter(tags=["Carts"], prefix="/cart")


# isn't that should be post ??!
@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_product_to_card(
    *,
    product_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> dict:
    """
    Given Product_Id Add it to a Cart if exists else create new Cart and then Insert it to CartItem
    Returns:
        dict: A message wit status code 201
    """
    email_address = "elon@tesla.com"
    return await add_to_cart(product_id, user_email=email_address, session=session)


@router.get("/")
async def read_cart(
    *,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CartPublic:
    email_address = "elon@tesla.com"
    return await get_all_cart_items(email_address, session)


@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_cart_item(  # noqa: ANN201
    *,
    cart_item_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    cart_item = session.get(CartItem, cart_item_id)
    await session.delete(cart_item)
    await session.commit()
    return {"ok": True}
