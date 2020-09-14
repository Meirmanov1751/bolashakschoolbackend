from rest_framework import permissions

from Course.models import Lesson, Category, Module


class HasLessonAccess(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_object_permission(self, request, view, obj):
        modules = Module.objects.filter(categories=obj.category).filter(moduleuser__user_id=request.user.id)
        if obj.free or modules.exists():
            lesson = Lesson.objects.filter(category=obj.category).filter(lesson_order=obj.lesson_order-1)
            if lesson.exists():
                lesson = lesson.first()
                history = lesson.lessonuserhistory_set.filter(user=request.user)
                if history.exists():
                    history = history.first()
                    print(history.mark)
                    if history.mark < lesson.task_min:
                        return False
                    return True
            else:
                return True
        return False
