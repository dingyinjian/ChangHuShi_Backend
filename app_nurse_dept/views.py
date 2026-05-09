from app_nurse_dept.models import NurseDept
from app_nurse_dept.serializers import NurseDeptSerializers
from utils.viewset import CustomModelViewSet
from rest_framework.decorators import action
from utils.json_response import SuccessResponse

def build_nurse_dept_tree(queryset):
    """把同一 queryset 里的部门按 parent 拼成树（根：parent 为空）。"""
    rows = list(queryset.order_by("sort", "-create_datetime"))
    children_map = {}
    for obj in rows:
        pid = obj.parent.id if obj.parent else None # 获取上级部门id
        children_map.setdefault(pid, []).append(obj)

    def to_node(obj):
        return {
            "id": obj.id,
            "dept_name": obj.dept_name,
            "dept_code": obj.dept_code,
            "parent": obj.parent.id if obj.parent else None,
            "sort": obj.sort,
            "status": obj.status,
            "children": [to_node(c) for c in children_map.get(obj.id, [])],
        }
    roots = children_map.get(None, [])
    return [to_node(r) for r in roots]

class NurseDeptViewSet(CustomModelViewSet):
    """
    长护师机构管理视图集 - 基础增删改查
    """
    queryset = NurseDept.objects.all()
    serializer_class = NurseDeptSerializers

    # 支持 ?status=0 过滤
    filterset_fields = ['status']

    # 支持 ?search=关键词 搜索
    search_fields = ['dept_name', 'dept_code']

    # 默认按创建时间倒序
    ordering = ['-create_datetime']

    @action(detail=False, methods=["get"], url_path="tree")
    def tree(self, request):
        qs = self.filter_queryset(self.get_queryset())
        data = build_nurse_dept_tree(qs)
        return SuccessResponse(data=data, msg="获取成功")