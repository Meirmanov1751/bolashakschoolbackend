from rest_framework.routers import DefaultRouter
from .views import CourseViewSet,CategoryViewSet, ModuleViewSet, LessonViewSet, CoursePriceViewSet
router = DefaultRouter()

router.register(r'^course', CourseViewSet)
router.register(r'^category', CategoryViewSet)
router.register(r'^module', ModuleViewSet)
router.register(r'^lesson', LessonViewSet)
router.register(r'^price', CoursePriceViewSet)