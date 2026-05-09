from rest_framework import serializers
from app_nurse.models import Nurse
from utils.serializers import CustomModelSerializer

class NurseSerializer(CustomModelSerializer):
    nurse_dept_name = serializers.CharField(source='nurse_dept.dept_name', read_only=True)
    class Meta:
        model = Nurse
        fields = "__all__"
        read_only_fields = ["id"]
    def validate_nurse_phone(self, value):
        if not value:
            return value
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError("请输入正确的手机号码")
        return value