from sqlmodel.ext.asyncio.session import AsyncSession

from e_store.products.models.categories import Category
from e_store.products.models.products import Product


async def create_new_category(category: Category, session: AsyncSession) -> Category:
    new_category = Category.model_validate(category)
    session.add(new_category)
    await session.commit()
    await session.refresh(new_category)
    return new_category


async def create_new_product(product: Product, session: AsyncSession) -> Product:
    new_product = Product.model_validate(product)
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    return new_product


async def verify_category_exists(
    category_id: str,
    session: AsyncSession,
) -> Category | None:
    return await session.get(Category, category_id)
