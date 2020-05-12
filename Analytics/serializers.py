from .models import AnalyticsCategory, Analytics, AnalyticsLesson
from rest_framework.serializers import ModelSerializer


class AnalyticsSerializer(ModelSerializer):
    class Meta:
        model = Analytics
        fields = '__all__'

class AnalyticsCategorySerializer(ModelSerializer):
    class Meta:
        model = AnalyticsCategory
        fields = '__all__'

class AnalyticsLessonSerializer(ModelSerializer):
    class Meta:
        model = AnalyticsLesson
        fields = '__all__'