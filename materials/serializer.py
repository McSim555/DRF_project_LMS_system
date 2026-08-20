from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_links
from users.models import Payment


class LessonSerializer(ModelSerializer):
    video_link = serializers.URLField(validators=[validate_links])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.subscription.filter(user=request.user).exists()
        return False


class CourseDetailSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, source="lesson")
    lessons_number = SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "name",
            "image",
            "description",
            "lessons",
            "lessons_number",
            "is_subscribed",
        ]

    def get_lessons_number(self, obj):
        return obj.lesson.count()

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.subscription.filter(user=request.user).exists()
        return False


# class SubscriptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Subscription
#         fields = ['id', 'user', 'course', 'created_at']
#         read_only_fields = ['user', 'created_at']
