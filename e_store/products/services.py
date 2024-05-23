from sqlmodel.ext.asyncio.session import AsyncSession

from e_store.products.models import Category


async def create_new_category(category: Category, session: AsyncSession) -> Category:
    new_category = Category.model_validate(category)
    session.add(new_category)
    await session.commit()
    await session.refresh(new_category)
    return new_category
