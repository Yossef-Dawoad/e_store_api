from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from e_store.cart.models.cart import Cart, CartItem, CartPublic
from e_store.products.models.products import Product
from e_store.shared.exceptions.http_400s import not_found_404_excep
from e_store.users.models.user import User


async def insert_into_itemCart(
    cart_id: int,
    product_id: int,
    session: AsyncSession,
) -> None:
    cart_item = CartItem(cart_id=cart_id, product_id=product_id)
    session.add(cart_item)
    await session.commit()
    await session.refresh(cart_item)


async def add_to_cart(product_id: int, session: AsyncSession) -> dict:
    # Get the Product By Id & Check if it exists and quanties more than one.
    product = await session.get(Product, product_id)
    if not product:
        raise not_found_404_excep(detail=f"Product with {product_id} Not Fount.!")
    if product.quantity <= 0:
        raise not_found_404_excep(detail=f"Product with {product_id} Is Out of Stock.!")

    # Getting User Info By his email
    user_stmt = select(User).where(User.email == "elon@tesla.com")
    user = (await session.exec(user_stmt)).first()

    # getting Cart Info if not Present will Create A New One
    cart_stmt = select(Cart).where(Cart.user_id == user.id)
    cart = (await session.exec(cart_stmt)).first()

    if not cart:
        cart = Cart(user_id=user.id)
        session.add(cart)
        await session.commit()
        await session.refresh(cart)

    await insert_into_itemCart(cart.id, product.id)
    return {"message": "Item Added to Cart"}


async def get_all_cart_items(session: AsyncSession) -> CartPublic | None:
    # Getting User Info with his email
    user_stmt = select(User).where(User.email == "elon@tesla.com")
    user = (await session.exec(user_stmt)).first()
    print("******" * 10)
    print(user)

    # getting Cart Info if not Present will Create A New One
    cart_stmt = select(Cart).where(Cart.user_id == user.id)
    cart = (await session.exec(cart_stmt)).first()
    print("******" * 10)
    print(cart)
    return cart
