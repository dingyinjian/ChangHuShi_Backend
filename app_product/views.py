from django.shortcuts import render

from app_product.models import Category, Product
from app_product.serializers import CategorySerializer, CategoryCreateUpdateSerializer, ProductSerializer, \
    ProductCreateUpdateSerializer
from utils.json_response import DetailResponse, ErrorResponse
from utils.viewset import CustomModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.db import transaction
# Create your views here.
class CategoryViewSet(CustomModelViewSet):
    queryset = Category.objects.all()
    #指定默认序列化器，用于：list列表和retrieve详情
    serializer_class = CategorySerializer
    create_serializer_class = CategoryCreateUpdateSerializer
    update_serializer_class = CategoryCreateUpdateSerializer
    #只有登录用户才能访问这些 API。
    permission_classes = [IsAuthenticated]
    #启用两种过滤方式：
    #DjangoFilterBackend → 支持精确字段过滤（如 ?is_active=true）
    #SearchFilter → 支持全局搜索（如 ?search=视频）
    filter_backends = [DjangoFilterBackend, SearchFilter]
    #声明哪些字段可以通过 ?字段名=值 进行精确过滤。
    filterset_fields = ['is_active']
    #声明哪些字段参与全文搜索（通过 ?search = 关键词）。
    search_fields = ['name', 'description']
    #数据库事务，它把一段代码包裹在一个数据库事务中
    # 如果这段代码任何地方抛出异常，Django 会自动 回滚（rollback）所有已执行的数据库操作
    # 如果全部成功，则自动 提交（commit）
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """重写删除逻辑，防止删除被商品引用的分类"""
        instance = self.get_object()
        try:
            #尝试删除（由于外键是 PROTECT，如果有商品关联会抛异常
            instance.delete()
            return DetailResponse(data=[],msg="删除成功")
        except Exception as e:
            # 捕获 ProtectedError 或其他数据库错误
            error_msg = str(e)
            if "PROTECT" in error_msg or "protected" in error_msg.lower():
                return ErrorResponse(data=[],msg="无法删除：该分类下存在关联商品，请先移除或转移商品")
            return ErrorResponse(data=[],msg=f"删除失败：{error_msg}")

class ProductViewSet(CustomModelViewSet):
    # 在执行主查询的同时，通过 SQL JOIN 把关联的数据也一并查出
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    create_serializer_class = ProductCreateUpdateSerializer
    update_serializer_class = ProductCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', 'is_active', 'delivery_type']
    search_fields = ['name', 'description','product_id']
