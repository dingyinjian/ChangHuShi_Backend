from rest_framework import serializers

from app_sop.models import Sop
from app_task.models import Task
from utils.serializers import CustomModelSerializer


class TaskSerializer(CustomModelSerializer):
    owner_name = serializers.CharField(source="owner.nurse_name", read_only=True)
    service_object_name = serializers.CharField(source="service_object.object_name", read_only=True)
    sop_items = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Sop.objects.all(),
        required=False,
        allow_empty=True,
    )
    sop_items_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["id"]

    def get_sop_items_detail(self, obj):
        return [{"id": s.id, "title": s.title} for s in obj.sop_items.all()]

    def create(self, validated_data):
        sop_items = validated_data.pop("sop_items", None)
        instance = super().create(validated_data)
        if sop_items is not None:
            instance.sop_items.set(sop_items)
        return instance

    def update(self, instance, validated_data):
        sop_items = validated_data.pop("sop_items", None)
        instance = super().update(instance, validated_data)
        if sop_items is not None:
            instance.sop_items.set(sop_items)
        return instance


class TaskApplyReportSerializer(serializers.Serializer):
    """YIBAOJUWEB 回写服务报告与分数"""

    service_report = serializers.CharField(required=True, allow_blank=False)
    service_score = serializers.DecimalField(
        max_digits=5, decimal_places=2, required=False, allow_null=True
    )
