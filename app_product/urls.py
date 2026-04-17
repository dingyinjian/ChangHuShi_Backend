"""
Time:     2026/2/11
Author:   公众号【布鲁的Python之旅】
Version:  V 0.1
File:     product/urls.py
Describe: 商品模块 API 路由
"""
from rest_framework import routers
from .views import CategoryViewSet, ProductViewSet

# 创建路由器
product_url = routers.SimpleRouter()

# 注册视图集
product_url.register(r'categories', CategoryViewSet)
product_url.register(r'products', ProductViewSet)

# 导出路由
urlpatterns = []
urlpatterns += product_url.urls