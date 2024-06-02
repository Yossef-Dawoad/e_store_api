from pydantic import EmailStr

from e_store.email_config import send_email


async def send_order_invoice_email(
    recipients: list[EmailStr],
    order_data: dict | None,
) -> None:
    await send_email(
        recipients=recipients,  # [user.email],
        subject="New Order Placed",
        context=order_data,
        template_name="order/order_creatation_invoice.html",
    )
