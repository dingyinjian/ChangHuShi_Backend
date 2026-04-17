from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from app_links.models import Link
from app_links.serializers import LinkSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser

class LinkViewSet(viewsets.ModelViewSet):
    """
    收藏链接视图集：提供完整的 CRUD 接口
    - list: 获取链接列表
    - retrieve: 查看单个链接
    - create: 创建新链接
    - update: 更新链接（全字段）
    - partial_update: 部分更新（如只改标题）
    - destroy: 删除链接
    """
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']  # 允许通过 ?category=xxx 筛选
    def perform_create(self, serializer):
        # 保存时自动将当前用户设为 owner
        serializer.save(owner=self.request.user)