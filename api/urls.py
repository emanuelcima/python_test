from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

from api.views import FieldViewSet, RainViewSet

router = DefaultRouter()
router.register(r'fields', FieldViewSet, basename='field')
router.register(r'rains', RainViewSet, basename='rain')

urlpatterns = router.urls
