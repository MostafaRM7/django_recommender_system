from rest_framework.routers import DefaultRouter

from .api_views import LoginViewSet

router = DefaultRouter()
router.register('login', LoginViewSet, basename='login')

urlpatterns = router.urls
