from rest_framework.routers import DefaultRouter
from .views import LessonViewSet, SubCategoryViewSet, CategoryViewSet
router = DefaultRouter()

router.register(r'^category', CategoryViewSet)
router.register(r'^sub-category', SubCategoryViewSet)
router.register(r'^lesson', LessonViewSet)