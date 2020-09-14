from rest_framework.routers import DefaultRouter
from .views import TestCategoryViewSet, TestGroupCategoryViewSet, TestGroupViewSet, TestCategoryPriceViewSet
router = DefaultRouter()

router.register(r'^test/category', TestCategoryViewSet)

router.register(r'^test/group', TestGroupViewSet)

router.register(r'^test/group_category', TestGroupCategoryViewSet)
router.register(r'^test/price', TestCategoryPriceViewSet)