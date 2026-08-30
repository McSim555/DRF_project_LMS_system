from smtplib import SMTPException

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from materials.models import Course
from users.models import User


@shared_task
def send_e_mail(user_id, course_id):
    try:
        user = User.objects.get(id=user_id)
        course = Course.objects.get(id=course_id)

        send_mail(
            subject='Обновление курса',
            message=f'Курс "{course.name}" был обновлен',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

    except User.DoesNotExist:
        error_msg = f"Пользователь с ID {user_id} не найден"
        return "Ошибка", error_msg

    except Course.DoesNotExist:
        error_msg = f"Курс с ID {course_id} не найден"
        return "Ошибка", error_msg

    except SMTPException as e:
        error_msg = f"SMTP ошибка: {str(e)}"
        return "Ошибка", error_msg

    except Exception as e:
        error_msg = f"Неизвестная ошибка: {str(e)}"
        return "Ошибка", error_msg