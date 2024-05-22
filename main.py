from fastapi import FastAPI


# # !TODO Remove when use alembic
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await init_db()
#     yield


# descripe the api that will be created
app = FastAPI(
    title="E-Commerce API",
    description="This is a simple E-Commerce API for CRUD operations on products and orders.",
    version="0.0.1",
    # lifespan=lifespan,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def hello(name: str):
    return {"message": f"Hello {name}"}
