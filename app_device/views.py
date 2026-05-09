from app_device.models import Device
from app_device.serializers import DeviceSerializers
from utils.viewset import CustomModelViewSet


class DeviceViewSet(CustomModelViewSet):
    """
    设备管理视图集 - 基础增删改查
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializers

    # 支持 ?status=0 过滤
    filterset_fields = ['status']

    # 支持 ?search=关键词 搜索
    search_fields = ['device_code', 'device_name', 'model', 'specification']

    # 默认按创建时间倒序
    ordering = ['-create_datetime']