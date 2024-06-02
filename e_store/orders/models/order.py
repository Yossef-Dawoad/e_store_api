import enum
from typing import TYPE_CHECKING, ClassVar, Optional

from sqlmodel import Column, Enum, Field, Relationship, SQLModel

from e_store.shared.models import SimpleIDModel, SimpleTimeStamp

if TYPE_CHECKING:
    from e_store.products.models.products import Product
    from e_store.users.models.user import User


class OrderStatus(enum.Enum):
    Processing = 1
    Packaging = 2
    Shipping = 3
    Shipped = 4


class OrderBase(SQLModel):
    total: float = Field(default=0.0)
    status: OrderStatus = Field(
        sa_column=Column(Enum(OrderStatus), default=OrderStatus.Processing),
    )

    user_id: int | None = Field(default=None, foreign_key="user.id")


class Order(OrderBase, SimpleIDModel, SimpleTimeStamp, table=True):
    order_items: list["OrderDetail"] = Relationship(back_populates="order")
    user: Optional["User"] = Relationship(back_populates="orders")


class OrderPublic(OrderBase, SimpleIDModel, SimpleTimeStamp):
    id: int


class OrderDetailBase(SQLModel):
    order_id: int | None = Field(default=None, foreign_key="order.id")
    product_id: int | None = Field(default=None, foreign_key="product.id")


class OrderDetail(OrderDetailBase, SimpleIDModel, table=True):
    quantity: int = Field(default=1)

    product: Optional["Product"] = Relationship(back_populates="order_detail")
    order: Optional["Order"] = Relationship(back_populates="order_items")


class OrderPublicWithOrderDetails(OrderPublic):
    order_items: ClassVar[list["OrderDetail"]] = []
