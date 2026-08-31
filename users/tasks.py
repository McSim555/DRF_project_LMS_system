from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def deactivate_user_by_last_login_date():
    cutoff_date = timezone.now() - timedelta(days=31)

    users_to_deactivate = User.objects.filter(
        is_active=True,
        last_login__lt=cutoff_date,
        is_superuser=False,
        is_staff=False,
    )

    count = users_to_deactivate.count()
    if count == 0:
        return {
            "status": "success",
            "deactivated_count": 0,
            "message": "Нет пользователей для деактивации",
        }

    deactivated_users = []
    for user in users_to_deactivate:
        deactivated_users.append(
            {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "last_login": (
                    user.last_login.strftime("%Y-%m-%d %H:%M:%S")
                    if user.last_login
                    else None
                ),
            }
        )

    updated_count = users_to_deactivate.update(is_active=False)

    return {
        "status": "success",
        "deactivated_count": updated_count,
        "message": f"Деактивировано {updated_count} пользователей",
        "users": deactivated_users,
    }
