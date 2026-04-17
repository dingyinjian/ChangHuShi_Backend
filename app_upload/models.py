from django.db import models

# Create your models here.
# fileupload/models.py
from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    original_name = models.CharField(max_length=255, verbose_name="原始文件名")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")
    file_size = models.PositiveIntegerField(verbose_name="文件大小（字节）")

    class Meta:
        verbose_name = "上传文件"
        verbose_name_plural = "上传文件"
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.original_name

    @property
    def url(self):
        return self.file.url