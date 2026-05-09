from rest_framework import routers

from app_task.views import TaskViewSet

system_url = routers.SimpleRouter()
system_url.register(r"task", TaskViewSet)

urlpatterns = system_url.urls
