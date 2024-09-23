from fastapi import BackgroundTasks

from e_store.authentication.hashing import hash_password
from e_store.config import get_settings
from e_store.email_config import send_email
from e_store.users.models.user import User

VERIFY_ACCOUNT_CTX = "verify-account"
FORGOT_PASSWORD_CTX = "password-reset"

settings = get_settings()


async def send_request_verification_email(
    user: User,
    background_tasks: BackgroundTasks,
) -> None:
    # user_token = create_ctx_token(
    #     context=VERIFY_ACCOUNT_CTX,
    #     password=user.hashed_password,
    #     current_time=datetime.now(tz=timezone.utc),
    # )
    verify_token = user.create_hashed_ctx(context=VERIFY_ACCOUNT_CTX)
    hashed_user_token = hash_password(verify_token)

    activate_url = f"""
    {settings.FRONTEND_HOST}/auth/account-verify?token={hashed_user_token}&email={user.email}
    """

    data = {
        "app_name": settings.app_name,
        "name": user.username,
        "activate_url": activate_url,
    }

    send_email(
        recipients=[user.email],
        subject=f"Account Verification - {settings.app_name}",
        template_name="user/account-request-verification.html",  # TODO Write the html templete
        context=data,
        background_tasks=background_tasks,
    )


async def send_welcome_verification_success_email(
    user: User,
    background_tasks: BackgroundTasks,
) -> None:
    data = {
        "app_name": settings.app_name,
        "name": user.username,
        # "login_uri": f"{settings.FRONTEND_Host}",
    }

    await send_email(
        recipients=[user.email],
        subject=f"Verification Success- {settings.app_name}",
        template_name="user/account-verification-success.html",  # TODO Write the html templete
        context=data,
        background_tasks=background_tasks,
    )
