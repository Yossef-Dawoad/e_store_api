from psycopg import IntegrityError
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from e_store.cart.models.cart import Cart, CartItem, CartItemPublic, CartPublic
from e_store.products.models.products import Product, ProductPublic
from e_store.shared.exceptions.http_400s import not_found_404_excep
from e_store.users.services import get_user_by_email


async def insert_into_itemcart(
    cart_id: int,
    product_id: int,
    session: AsyncSession,
) -> None:
    cart_item = CartItem(cart_id=cart_id, product_id=product_id)
    session.add(cart_item)
    await session.commit()
    await session.refresh(cart_item)


async def add_to_cart(product_id: int, user_email: str, session: AsyncSession) -> dict:
    # Get the Product By Id & Check if it exists and quanties more than one.
    product = await session.get(Product, product_id)
    if not product:
        raise not_found_404_excep(detail=f"Product with id {product_id} not found")
    if product.quantity <= 0:
        raise not_found_404_excep(detail=f"Product with id {product_id} is out of stock")

    user = await get_user_by_email(user_email, session)
    cart = await get_or_create_cart(user.id, session)

    # Check if the item is already in the cart
    stmt = select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == product.id)
    cart_item = (await session.exec(stmt)).first()
    if cart_item:
        # If the item is already in the cart, increment the quantity
        cart_item.quantity += 1
        cart_item.subtotal = cart_item.quantity * product.price
    else:
        # If it's a new item, create a new CartItem
        cart_item = CartItem(cart_id=cart.id, product_id=product.id, subtotal=product.price)
        session.add(cart_item)

    # Decrease product quantity
    product.quantity -= 1
    session.add(product)
    try:
        await session.commit()
    except IntegrityError as err:
        await session.rollback()
        raise not_found_404_excep(detail="Error adding item to cart. Please try again.") from err

    await session.commit()
    return {"message": "Item added to cart"}


async def get_or_create_cart(user_id: int, session: AsyncSession) -> Cart:
    cart = await session.exec(select(Cart).where(Cart.user_id == user_id))
    cart = cart.first()
    if not cart:
        cart = Cart(user_id=user_id)
        session.add(cart)
        await session.commit()
        await session.refresh(cart)
    return cart


async def get_all_cart_items(user_email: str, session: AsyncSession) -> CartPublic:
    user = await get_user_by_email(user_email, session)

    cart_stmt = (
        select(Cart)
        .where(Cart.user_id == user.id)
        .options(selectinload(Cart.items).selectinload(CartItem.product))
    )
    cart = (await session.exec(cart_stmt)).first()
    print("*******" * 10)
    print(cart)
    print("*******" * 10)

    if cart is None:
        raise not_found_404_excep(detail=f"There is NO Current Cart for User with  {user.id = } ...!")
    return CartPublic(
        id=cart.id,
        user_id=cart.user_id,
        items=[
            CartItemPublic(
                # product_id=item.product_id,
                # quantity=item.quantity,
                # subtotal=item.subtotal,
                product=ProductPublic(**item.product.model_dump()),
            )
            for item in cart.items
        ],
    )
