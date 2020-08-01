from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

from api.views import FieldViewSet, RainViewSet

router = routers.SimpleRouter()
router.register(r'fields', FieldViewSet, basename='field')
router.register(r'rains', RainViewSet)

urlpatterns = router.urls
urlpatterns = format_suffix_patterns(router.urls)
