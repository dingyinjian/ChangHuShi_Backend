"""
URL configuration for application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from app_login.views import CaptchaView, LoginView
from application import settings
from django.conf.urls.static import static  # 👈 导入
urlpatterns = [
    path('getCaptcha/', CaptchaView.as_view()),
    path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path('admin/', admin.site.urls),
    path('system/', include('app_post.urls')),
    path('system/', include('app_dept.urls')),
    path('system/', include('app_apis.urls')),
    path('system/', include('app_menu.urls')),
    path('system/', include('app_role.urls')),
    path('system/', include('app_dict.urls')),
    path('system/', include('app_user.urls')),
    path('system/', include('app_operation_log.urls')),
    path('system/', include('app_message.urls')),
    path('system/', include('app_example.urls')),
    path('job/crontab/', include('app_crontab.urls')),
    path('tool/', include('app_monitor.urls')),
    path('link/', include('app_links.urls')),
    path('api/',include('app_upload.urls')),
    path('api/',include('app_device.urls')),
    path('api/',include('app_nurse_dept.urls')),
    path('api/',include('app_nurse.urls')),
    path('api/',include('app_service_object.urls')),
    path('system/', include('app_sop.urls')),
    path('system/', include('app_task.urls')),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)