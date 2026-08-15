from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
)

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("courses", CourseViewSet, basename="course")

urlpatterns = [
    path("lesson/create/", LessonCreateAPIView.as_view(), name="create_lesson"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="detail_lesson"),
    path("lessons/", LessonListAPIView.as_view(), name="list_lessons"),
    path(
        "lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="delete_lesson"
    ),
    path(
        "lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="update_lesson"
    ),
]

urlpatterns += router.urls
