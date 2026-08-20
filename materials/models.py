from django.db import models

from users.models import User


class Course(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    image = models.ImageField(
        upload_to="materials/images/courses/",
        verbose_name="Превью",
        help_text="Вставьте изображение",
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Вставьте описание курса",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец курса",
        help_text="Введите владельца курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Вставьте описание курса",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="materials/images/lessons/",
        verbose_name="Превью",
        help_text="Вставьте изображение",
        blank=True,
        null=True,
    )
    video_link = models.URLField(
        verbose_name="Ссылка на видеоурок",
        help_text="Вставьте ссылку на видео",
        blank=True,
        null=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Выберите курс",
        related_name="lesson",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец урока",
        help_text="Введите владельца урока",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
