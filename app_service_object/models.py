from django.db import models
from utils.models import BaseModel
# Create your models here.
class ServiceObject(BaseModel):
    object_name = models.CharField(max_length=32,verbose_name="姓名",help_text="姓名")
    object_phone = models.CharField(max_length=11,verbose_name="手机号",help_text="手机号")
    GENDER_CHOICES = (
        ('0', "男"),
        ('1', "女")
    )
    object_gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default="0",verbose_name="性别",help_text="性别")
    id_card = models.CharField(max_length=18,verbose_name="身份证号",null=True,blank=True,help_text="身份证号")
    object_birthday = models.DateField(verbose_name="出生日期",null=True,blank=True,help_text="出生日期")
    object_address = models.CharField(max_length=255,verbose_name="地址",null=True,blank=True,help_text="地址")
    object_remark = models.CharField(max_length=255,verbose_name="备注",null=True,blank=True,help_text="备注")
    STATUS_CHOICES = (
        ('0', "正常"),
        ('1', "暂停"),
        ('2', "终止"),
    )
    service_status = models.CharField(max_length=1,choices=STATUS_CHOICES,default="0",verbose_name="状态",help_text="状态")
    nurse_dept = models.ForeignKey("app_nurse_dept.NurseDept",on_delete=models.PROTECT,db_constraint=False,verbose_name="所属机构",help_text="所属机构",null=True,blank=True,)
    nurse = models.ForeignKey("app_nurse.Nurse",on_delete=models.PROTECT,db_constraint=False,verbose_name="责任长护师",help_text="责任长护师",null=True,blank=True,)
    class Meta:
        db_table = "app_service_object"
        verbose_name = "服务对象管理"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)
    def __str__(self):
        return self.object_name