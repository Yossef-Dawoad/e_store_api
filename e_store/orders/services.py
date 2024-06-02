from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from e_store.cart.models import Cart, CartItem
from e_store.orders.models import Order, OrderDetail, OrderPublic
from e_store.shared.exceptions.http_400s import bad_400_excep
from e_store.users.models.user import User

from . import tasks


async def create_new_order(session: AsyncSession) -> OrderPublic:
    # Getting User Info with his email
    user_stmt = select(User).where(User.email == "elon@tesla.com")
    user = (await session.exec(user_stmt)).first()

    # getting Cart Info
    cart_stmt = select(Cart).where(Cart.user_id == user.id)
    cart = (await session.exec(cart_stmt)).first()

    cart_items_stmt = select(CartItem).where(Cart.id == cart.id)
    cart_items = (await session.exec(cart_items_stmt)).all()
    if len(cart_items) <= 0:
        bad_400_excep(detail="No Items found In Cart !")

    total_amount = 0.0
    for item in cart_items:
        total_amount += item.products.price

    new_order = Order(
        total=total_amount,
        user_id=user.id,
        shipping_address="Cairo, DownTown",
    )
    session.add(new_order)
    await session.commit()
    await session.refresh(new_order)

    session.add_all(
        [OrderDetail(order_id=new_order.id, product_id=item.products.id) for item in cart_items],
    )
    await session.commit()

    # TODO send an email
    # tasks.send_invoice_email_task.delay("the email")

    # Clear items in the cart
    cart_items_stmt = select(CartItem).where(CartItem.cart_id == cart.id)
    await session.delete(cart_items_stmt)
    await session.commit()

    return new_order


async def get_list_of_order(session: AsyncSession) -> list[Order]:
    # Getting User Info with his email
    user_stmt = select(User).where(User.email == "elon@tesla.com")
    user = (await session.exec(user_stmt)).first()

    # getting Order Info
    order_stmt = select(Order).where(Order.user_id == user.id)
    orders = (await session.exec(order_stmt)).all()
    return orders
