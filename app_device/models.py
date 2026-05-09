from django.db import models
from utils.models import BaseModel, table_prefix


class Device(BaseModel):
    # unique=True 表示这个字段在数据库里必须“唯一值”，不能重复。
    device_code = models.CharField(max_length=64,unique=True,verbose_name="设备编号",help_text="设备编号",)
    device_name = models.CharField(max_length=64,verbose_name="设备名称",help_text="设备名称",)
    model = models.CharField(max_length=64,null=True,blank=True,verbose_name="型号",help_text="型号",)
    specification = models.CharField(max_length=128,null=True,blank=True,verbose_name="规格",help_text="规格",)
    STATUS_CHOICES = (("0", "正常"),("1", "停用"),)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default="0",verbose_name="设备状态（0正常 1停用）",help_text="设备状态（0正常 1停用）",)

    class Meta:
        db_table = "app_device"
        verbose_name = "设备管理"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)