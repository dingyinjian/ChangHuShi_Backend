# serializers.py
from rest_framework import serializers
from app_links.models import Link
from app_user.models import Users
import json

class LinkSerializer(serializers.ModelSerializer):
    # 输出时显示 owner 的用户名
    owner_name = serializers.CharField(source='owner.username', read_only=True)

    # 接收前端传入的图片 URL 列表（仅用于写入）
    images = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="上传后的图片URL列表"
    )

    owner = serializers.PrimaryKeyRelatedField(
        queryset=Users.objects.all(),
        required=False
    )

    class Meta:
        model = Link
        fields = [
            'id',
            'title',
            'url',
            'category',
            'description',
            'is_active',
            'owner',
            'owner_name',
            'images',  # 前端交互使用 images 字段
            'create_time',
            'update_time',
        ]
        read_only_fields = ['create_time', 'update_time']

    def to_representation(self, instance):
        """覆盖默认行为，确保输出包含 images 字段"""
        data = super().to_representation(instance)
        try:
            data['images'] = json.loads(instance.image_urls) if instance.image_urls else []
        except (TypeError, ValueError):
            data['images'] = []
        return data

    def validate_images(self, value):
        """可选：验证 images 列表中的每个 URL 是否合法"""
        for url in value:
            if not isinstance(url, str):
                raise serializers.ValidationError("每个图片 URL 必须是字符串")
        return value

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['owner'] = request.user
        else:
            raise serializers.ValidationError("无法获取当前用户")

        # 将 images 转为 JSON 字符串存入 database 的 image_urls 字段
        validated_data['image_urls'] = json.dumps(images, ensure_ascii=False)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        #从字典中删除指定的键（key），并返回对应的值（value）。
        images = validated_data.pop('images', None)

        # 更新普通字段
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # 如果传了 images，则更新
        if images is not None:
            instance.image_urls = json.dumps(images, ensure_ascii=False)

        instance.save()
        return instance