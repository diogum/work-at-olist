from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, base_name='categories')

urlpatterns = router.urls
