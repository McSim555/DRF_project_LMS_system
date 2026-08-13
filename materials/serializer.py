from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

class CourseDetailSerializer(ModelSerializer):
    lessons_number = SerializerMethodField()
    class Meta:
        model = Course
        fields = ['name', 'image', 'description', 'lessons_number']

    def get_lessons_number(self, obj):
            return obj.lesson.count()


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
