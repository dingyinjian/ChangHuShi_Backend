from rest_framework import routers
from app_nurse.views import NurseViewSet

router = routers.SimpleRouter()
router.register(r'nurses', NurseViewSet, basename='nurses')

urlpatterns = router.urls