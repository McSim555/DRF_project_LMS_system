from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None
    email = models.EmailField(
        max_length=255, unique=True, verbose_name="Email", help_text="Укажите e-mail"
    )
    phone = models.CharField(
        max_length=11,
        verbose_name="Номер телефона",
        blank=True,
        null=True,
        help_text="Укажите номер телефона",
    )
    avatar = models.ImageField(
        upload_to="users/images/",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Вставьте аватар",
    )
    city = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


PAYMENT_CHOICES = [
    ("cash", "Наличные"),
    ("transfer", " на счет"),
]


class Payment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Платеж",
        help_text="Выберите платеж",
        related_name="payment",
    )
    payment_date = models.DateField(
        verbose_name="Дата платежа", help_text="Введите дату платежа"
    )
    paid_course = models.ForeignKey(
        "materials.Course",
        on_delete=models.CASCADE,
        verbose_name="Оплаченный курс",
        help_text="Выберите курс",
        related_name="paid_course",
        blank=True,
        null=True,
    )
    paid_lesson = models.ForeignKey(
        "materials.Lesson",
        on_delete=models.CASCADE,
        verbose_name="Оплаченный урок",
        help_text="Выберите урок",
        related_name="paid_lesson",
        blank=True,
        null=True,
    )
    paid_amount = models.DecimalField(
        verbose_name="Сумма платежа",
        help_text="Введите сумму платежа",
        max_digits=10,
        decimal_places=2,
        default=0.00,
        null=True,
        blank=True,
    )
    payment_type = models.CharField(
        choices=PAYMENT_CHOICES,
        verbose_name="Способ платежа",
        help_text="Выберите способ платежа",
    )
