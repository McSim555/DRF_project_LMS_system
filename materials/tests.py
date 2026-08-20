from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@test.ru", password="123")
        self.course = Course.objects.create(name="test", description="test")
        self.lesson = Lesson.objects.create(
            name="test", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:detail_lesson", kwargs={"pk": self.lesson.pk})
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["name"], "test")

    def test_lesson_create(self):
        url = reverse("materials:create_lesson")
        data = {"name": "test", "course": self.course.pk, "owner": self.user.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("materials:update_lesson", kwargs={"pk": self.lesson.pk})
        response = self.client.patch(url)
        data = {"name": "test3"}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["name"], "test3")

    def test_lesson_delete(self):
        url = reverse("materials:delete_lesson", kwargs={"pk": self.lesson.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:list_lessons")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "video_link": None,
                    "owner": self.user.pk,
                    "name": self.lesson.name,
                    "description": None,
                    "image": None,
                    "course": self.course.pk,
                },
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
