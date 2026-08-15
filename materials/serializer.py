from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson
from users.models import Payment


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, source="lesson")
    lessons_number = SerializerMethodField()

    class Meta:
        model = Course
        fields = ["name", "image", "description", "lessons", "lessons_number"]

    def get_lessons_number(self, obj):
        return obj.lesson.count()

