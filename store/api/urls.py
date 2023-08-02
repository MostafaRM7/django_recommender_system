from rest_framework.routers import DefaultRouter

from .api_views import ProductViewSet, CategoryViewSet, HomeViewSet

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)
router.register('home', HomeViewSet)

urlpatterns = router.urls
