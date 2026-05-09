from import_export.fields import Field
from import_export import resources

from app_nurse_dept.models import NurseDept
from utils.serializers import CustomModelSerializer


class NurseDeptSerializers(CustomModelSerializer):
    class Meta:
        model = NurseDept
        fields = "__all__"
        read_only_fields = ["id"]