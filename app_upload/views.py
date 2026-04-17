from django.shortcuts import render

# Create your views here.
# fileupload/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import FileUploadSerializer
from .models import UploadedFile


class SingleFileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.save()
            return Response({
                'url': uploaded_file.url,
                'id': uploaded_file.id,
                'original_name': uploaded_file.original_name
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MultipleFileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('files')  # 前端字段名必须是 'files'
        if not files:
            return Response({'error': '未选择文件'}, status=status.HTTP_400_BAD_REQUEST)

        results = []
        errors = []

        for f in files:
            serializer = FileUploadSerializer(data={'file': f})
            if serializer.is_valid():
                uploaded = serializer.save()
                results.append({
                    'url': uploaded.url,
                    'id': uploaded.id,
                    'original_name': uploaded.original_name
                })
            else:
                errors.append({'file': f.name, 'errors': serializer.errors})

        if errors:
            return Response({
                'success': results,
                'failed': errors
            }, status=status.HTTP_207_MULTI_STATUS)  # 207 表示部分成功

        return Response(results, status=status.HTTP_201_CREATED)