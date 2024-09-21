from datetime import datetime, timezone

from fastapi import BackgroundTasks

from e_store.authentication.hashing import create_ctx_token, hash_password
from e_store.config import get_settings
from e_store.email_config import send_email
from e_store.users.models.user import User

FORGOT_PASSWORD_CTX = "verify-account"  # noqa: S105
VERIFY_ACCOUNT_CTX = "password-reset"

settings = get_settings()


async def send_request_verification_email(
    user: User,
    background_tasks: BackgroundTasks,
) -> None:
    user_token = create_ctx_token(
        context=VERIFY_ACCOUNT_CTX,
        password=user.password,
        current_time=datetime.now(tz=timezone.utc),
    )
    hashed_user_token = hash_password(user_token)

    activate_url = f"""
    {settings.FRONTEND_HOST}/auth/account-verify?token={hashed_user_token}&email={user.email}
    """

    data = {
        "app_name": settings.app_name,
        "name": user.username,
        "activate_url": activate_url,
    }

    await send_email(
        recipients=[user.email],
        subject=f"Account Verification - {settings.app_name}",
        template_name="user/account-request-verification.html",
        context=data,
        background_tasks=background_tasks,
    )
