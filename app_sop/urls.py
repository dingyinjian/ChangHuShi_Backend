from rest_framework import routers
from app_sop.views import SopViewSet

system_url = routers.SimpleRouter()
system_url.register(r"sop", SopViewSet)

urlpatterns = system_url.urls
