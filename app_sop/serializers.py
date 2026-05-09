
from app_sop.models import Sop
from utils.serializers import CustomModelSerializer

class SopSerializer(CustomModelSerializer):
    class Meta:
        model = Sop
        fields = "__all__"
        read_only_fields = ["id"]

class SopCreateUpdateSerializer(CustomModelSerializer):
    class Meta:
        model = Sop
        fields = [
            "id",
            "title",
            "content_html",
            "video_url",
            "analysis_result",
            "analysis_status",
            "analysis_error",
        ]
        # 创建时由模型 Snowflake 生成 id，前端不必传
        read_only_fields = ["id"]
