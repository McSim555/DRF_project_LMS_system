from django.contrib.auth.models import AbstractUser
from django.db import models


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

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
