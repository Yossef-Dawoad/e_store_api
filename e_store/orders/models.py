import enum
from typing import TYPE_CHECKING

from sqlmodel import Column, Enum, Field, Relationship, SQLModel

from e_store.shared.models import SimpleIDModel, SimpleTimeStamp

if TYPE_CHECKING:
    from e_store.products.models.products import Product
    from e_store.users.models import User


class OrderStatus(enum.Enum):
    Processing = 1
    Packaging = 2
    Shipping = 3
    Shipped = 4


class OrderBase(SQLModel):
    total: float = Field(default=0.0)
    shipping_address: str
    status: OrderStatus = Field(
        sa_column=Column(Enum(OrderStatus), default=OrderStatus.Processing),
    )

    user_id: int | None = Field(default=None, foreign_key="user.id")


class Order(OrderBase, SimpleIDModel, SimpleTimeStamp, table=True):
    order_detail: "OrderDetail" | None = Relationship(back_populates="order")  # list
    user: "User" | None = Relationship(back_populates="order")


# TODO To Include list[orderDetail]
class OrderPublic(OrderBase, SimpleIDModel, SimpleTimeStamp):
    pass


class OrderDetailBase(SQLModel):
    order_id: int | None = Field(default=None, foreign_key="order.id")
    product_id: int | None = Field(default=None, foreign_key="product.id")


class OrderDetail(OrderDetailBase, SimpleIDModel, SimpleTimeStamp, table=True):
    quantity: int = Field(default=1)

    product: "Product" | None = Relationship(back_populates="order_detail")
    order: "Order" | None = Relationship(back_populates="order_detail")


# TODO To Include list[orderDetail]
class OrderDetailPublic(OrderDetailBase, SimpleIDModel):
    pass
