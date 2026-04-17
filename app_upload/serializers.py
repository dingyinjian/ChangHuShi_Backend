# fileupload/serializers.py
from rest_framework import serializers
from .models import UploadedFile

class FileUploadSerializer(serializers.ModelSerializer):
    # 前端传 file 字段，这里接收
    file = serializers.FileField(write_only=True)  # write_only 表示只用于输入
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UploadedFile
        fields = ['file', 'url', 'original_name', 'file_size']
        read_only_fields = ['url', 'original_name', 'file_size']

    def get_url(self, obj):
        return obj.file.url if obj.file else None

    def create(self, validated_data):
        file = validated_data['file']
        instance = UploadedFile.objects.create(
            file=file,
            original_name=file.name,
            file_size=file.size,
        )
        return instance