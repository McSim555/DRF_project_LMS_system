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

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


PAYMENT_CHOICES = [
    ('cash', 'Наличные'),
    ('transfer', ' на счет'),
]


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Платеж",
        help_text="Выберите платеж", related_name="payment")
    payment_date = models.DateField(verbose_name='Дата платежа', help_text='Введите дату платежа')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Оплаченный курс",
        help_text="Выберите курс", related_name="paid_course", blank=True, null=True)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Оплаченный урок",
        help_text="Выберите урок", related_name="paid_lesson", blank=True, null=True)
    paid_amount = models.DecimalField(verbose_name='Сумма платежа', help_text='Введите сумму платежа', max_digits=10,
    decimal_places=2, default=0.00, null=True, blank=True)
    payment_type = models.CharField(choices=PAYMENT_CHOICES, verbose_name='Способ платежа', help_text='Выберите способ платежа')