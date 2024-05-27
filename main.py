import logging

from fastapi import FastAPI

from e_store.cart.router import cart_router
from e_store.orders.router import order_router
from e_store.products.router import category_router, products_router
from e_store.users.router import user_router
from logs.log import init_loggers

# # !TODO Remove when use alembic
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await init_db()
#     yield

# init our logger
init_loggers(logger_name="estore-logs")
log = logging.getLogger("estore-logs")

# descripe the api that will be created
app = FastAPI(
    title="E-Commerce API",
    description="This is a Simple e-store API for CRUD operations on products and orders.",
    version="0.0.1",
    # lifespan=lifespan,
)


app.include_router(user_router)
app.include_router(category_router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(order_router)


@app.get("/health-check")
def health_check() -> dict:
    return {"status": r"100% good"}
