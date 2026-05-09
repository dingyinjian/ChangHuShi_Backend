from rest_framework import routers
from app_device.views import DeviceViewSet

device_url = routers.SimpleRouter()
device_url.register(r'devices', DeviceViewSet)

urlpatterns = device_url.urls