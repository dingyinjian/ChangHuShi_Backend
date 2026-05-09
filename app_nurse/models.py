from django.db import models
from utils.models import BaseModel

class Nurse(BaseModel):
    nurse_name = models.CharField(max_length=10,verbose_name="姓名",help_text="姓名",)
    nurse_code = models.CharField(max_length=64,unique=True,verbose_name="编号",help_text="编号",)
    nurse_role = models.CharField(max_length=64,verbose_name="角色",help_text="角色",null=True,blank=True,)
    nurse_dept = models.ForeignKey("app_nurse_dept.NurseDept",on_delete=models.PROTECT,db_constraint=False,verbose_name="所属机构",help_text="所属机构",null=True,blank=True,)
    nurse_phone = models.CharField(max_length=11,verbose_name="手机号",help_text="手机号",null=True,blank=True,)
    STATUS_CHOICES = (("0", "在职"),("1", "离职"),)
    nurse_status = models.CharField(max_length=1,choices=STATUS_CHOICES,default="0",verbose_name="在职状态（0在职 1离职）",help_text="在职状态（0在职 1离职）")
    nurse_remark = models.CharField(max_length=255,verbose_name="备注",help_text="备注",null=True,blank=True,)
    class Meta:
        db_table ="app_nurse"
        verbose_name = "长护师人员"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)
    def __str__(self):
        return self.nurse_name
