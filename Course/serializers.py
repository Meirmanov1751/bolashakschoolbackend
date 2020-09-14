from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from .models import Lesson, Category, Course, Module, LessonTasks, LessonUserHistory


class LessonUserHistorySerializer(ModelSerializer):
    class Meta:
        model = LessonUserHistory
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ModuleSerializer(ModelSerializer):
    closed = serializers.SerializerMethodField('get_closed')

    def get_closed(self, obj):
        user = self.context['request'].user
        modules = obj.moduleuser_set.filter(user=user).filter(verified=True)
        if modules.exists():
            return False
        return True

    class Meta:
        model = Module
        fields = '__all__'


class LessonTaskSerializer(ModelSerializer):
    class Meta:
        model = LessonTasks
        fields = '__all__'


class LessonClosedSerializer(ModelSerializer):
    closed = serializers.SerializerMethodField('get_closed')

    def get_closed(self, obj):
        return True

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'closed')


class LessonDetailedSerializer(ModelSerializer):
    tasks = LessonTaskSerializer(many=True)
    history = serializers.SerializerMethodField('get_history')

    def get_history(self, obj):
        user = self.context['request'].user
        history = obj.lessonuserhistory_set.filter(user=user)
        print(history)
        if len(history) > 0:
            serializer = LessonUserHistorySerializer(history.first())
            return serializer.data
        return None

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    modules = ModuleSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'


class CategoryDetailedSerializer(ModelSerializer):
    lessons_list = serializers.SerializerMethodField('get_lessons')

    def get_lessons(self, obj):
        user = self.context['request'].user
        lessons = obj.lessons.all().order_by('lesson_order')
        lessons_list = []
        modules = obj.module.moduleuser_set.filter(user=user).filter(verified=True)
        for lesson in lessons:
            lesson_prev = Lesson.objects.filter(category=lesson.category).filter(lesson_order=lesson.lesson_order - 1)
            serializer = LessonClosedSerializer(lesson)
            if lesson.free or modules.exists():
                if lesson_prev.exists():
                    lesson_prev = lesson_prev.first()
                    history = lesson_prev.lessonuserhistory_set.filter(user=user)
                    print('history', history)
                    if history.exists():
                        history = history.first()
                        if history.mark >= lesson_prev.task_min:
                            serializer = LessonSerializer(lesson)
                else:
                    serializer = LessonSerializer(lesson)
            lessons_list.append(serializer.data)
        return lessons_list

    class Meta:
        model = Category
        fields = '__all__'


class ModuleDetailedSerializer(ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = Module
        fields = '__all__'


class FilteredListSerializer(serializers.ListSerializer):

    def to_representation(self, instance):
        print(instance)
        instance = instance.exclude(moduleuser__user_id=self.context['request'].user.id,
                                    moduleuser__verified=True)
        return super(FilteredListSerializer, self).to_representation(instance)


class ModuleDetailedPriceSerializer(ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = Module
        fields = '__all__'


class CoursePriceSerializer(ModelSerializer):
    modules = ModuleDetailedPriceSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'
