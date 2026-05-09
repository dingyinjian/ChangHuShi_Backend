from import_export.fields import Field
from import_export import resources

from app_device.models import Device
from utils.serializers import CustomModelSerializer


class DeviceSerializers(CustomModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"
        read_only_fields = ["id"]


class DeviceResource(resources.ModelResource):
    id = Field(attribute='id', column_name=Device.id.field.verbose_name)
    device_code = Field(attribute='device_code', column_name=Device.device_code.field.verbose_name)
    device_name = Field(attribute='device_name', column_name=Device.device_name.field.verbose_name)
    model = Field(attribute='model', column_name=Device.model.field.verbose_name)
    specification = Field(attribute='specification', column_name=Device.specification.field.verbose_name)
    status = Field(attribute='status', column_name=Device.status.field.verbose_name)
    update_datetime = Field(attribute='update_datetime', column_name=Device.update_datetime.field.verbose_name)
    create_datetime = Field(attribute='create_datetime', column_name=Device.create_datetime.field.verbose_name)

    class Meta:
        model = Device
        fields = (
            'id',
            'device_code',
            'device_name',
            'model',
            'specification',
            'status',
            'update_datetime',
            'create_datetime',
        )
        export_order = fields