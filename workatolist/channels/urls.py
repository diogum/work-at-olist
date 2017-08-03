from rest_framework.routers import DefaultRouter

from .views import ChannelViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'channels', ChannelViewSet)
router.register(r'categories', CategoryViewSet, base_name='categories')

urlpatterns = router.urls
