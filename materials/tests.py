from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_links
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

    def test_lesson_create_unauthenticated(self):
        self.client.logout()
        url = reverse("materials:create_lesson")
        data = {"name": "test", "course": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_retrieve_unauthenticated(self):
        self.client.logout()
        url = reverse("materials:detail_lesson", kwargs={"pk": self.lesson.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_list_unauthenticated(self):
        self.client.logout()
        url = reverse("materials:list_lessons")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_update_unauthenticated(self):
        self.client.logout()
        url = reverse("materials:update_lesson", kwargs={"pk": self.lesson.pk})
        data = {"name": "updated_name"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_delete_unauthenticated(self):
        self.client.logout()
        url = reverse("materials:delete_lesson", kwargs={"pk": self.lesson.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_moderator_can_create_lesson(self):
        self.moderator = User.objects.create_user(
            email="moderator@test.ru", password="123"
        )
        moderator_group, _ = Group.objects.get_or_create(name="moderators")
        self.moderator.groups.add(moderator_group)
        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:create_lesson")
        data = {"name": "moderator_lesson", "course": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_moderator_can_update_any_lesson(self):
        self.moderator = User.objects.create_user(
            email="moderator@test.ru", password="123"
        )
        moderator_group, _ = Group.objects.get_or_create(name="moderators")
        self.moderator.groups.add(moderator_group)
        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:update_lesson", kwargs={"pk": self.lesson.pk})
        data = {"name": "updated_by_moderator"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@test.ru", password="123")
        self.other_user = User.objects.create_user(
            email="other@test.ru", password="123"
        )
        self.course = Course.objects.create(name="Test Course")
        self.client.force_authenticate(user=self.user)

    def test_subscribe_to_course(self):
        url = reverse("materials:subscription-toggle")
        data = {"course": self.course.pk, "user": self.user.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка добавлена")
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_unsubscribe_from_course(self):
        Subscription.objects.create(course=self.course, user=self.user)
        url = reverse("materials:subscription-toggle")
        data = {"course": self.course.pk, "user": self.user.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка удалена")
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )


class ValidateLinksTest(APITestCase):

    def test_valid_links(self):
        valid_links = [
            "https://youtube.com/watch?v=abc123",
            "https://www.youtube.com/watch?v=xyz",
        ]
        for link in valid_links:
            try:
                validate_links(link)
            except ValidationError:
                self.fail(f"Ссылка на {link} недопустима")

    def test_invalid_links(self):
        invalid_links = [
            "https://google.com",
            "https://yandex.ru",
        ]
        for link in invalid_links:
            with self.assertRaises(ValidationError) as context:
                validate_links(link)
            self.assertIn(f"Ссылка на {link} недопустима", str(context.exception))
