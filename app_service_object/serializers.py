from rest_framework import serializers
from app_service_object.models import ServiceObject
from utils.serializers import CustomModelSerializer

class ServiceObjectSerializer(CustomModelSerializer):
    nurse_dept_name = serializers.CharField(source='nurse_dept.dept_name', read_only=True)
    nurse_name = serializers.CharField(source='nurse.nurse_name', read_only=True)
    class Meta:
        model = ServiceObject
        fields = "__all__"
        read_only_fields = ["id"]
    def validate_object_phone(self, value):
        if not value:
            return value
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError("请输入正确的手机号码")
        return value
    def validate_id_card(self, value):
        if not value:
            return value
        if len(value) not in (15,18):
            raise serializers.ValidationError("请输入正确的身份证号码")
        return value