from rest_framework import routers
from app_nurse_dept.views import NurseDeptViewSet

router = routers.SimpleRouter()
router.register(r'nurse-dept', NurseDeptViewSet, basename='nurse-dept')

urlpatterns = router.urls