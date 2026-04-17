# app_links/urls.py
from django.urls import re_path
from rest_framework.routers import SimpleRouter
from .views import LinkViewSet

# 创建路由器，注册标准 CRUD 接口
router = SimpleRouter()
router.register(r'list', LinkViewSet, basename='link')

# 如果将来要加自定义接口，比如：
# - 按分类统计
# - 导出为 HTML
# - 批量导入
# 可以在这里添加

urlpatterns = [
    # 示例：将来可以加一个统计接口
    # re_path('links/stats/', LinkViewSet.as_view({'get': 'stats'})),
]

# 合并：自定义接口 + 自动生成的 CRUD




urlpatterns += router.urls