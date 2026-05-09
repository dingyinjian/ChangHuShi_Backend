from rest_framework import routers
from app_service_object.views import ServiceObjectViewSet

router = routers.SimpleRouter()
router.register(r'service-object', ServiceObjectViewSet, basename='service-object')

urlpatterns = router.urls