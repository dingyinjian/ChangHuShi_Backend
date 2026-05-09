from django.db import models
from utils.models import BaseModel


class NurseDept(BaseModel):
    """长护师业务侧部门（与系统用户、app_dept 组织无强制关联）。"""

    dept_name = models.CharField(max_length=64, verbose_name="部门名称", help_text="部门名称")
    dept_code = models.CharField(
        max_length=64,
        unique=True,
        null=True,
        blank=True,
        verbose_name="部门编码",
        help_text="部门编码",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="上级部门",
        help_text="空表示顶级部门",
        db_constraint=False,
        related_name="children",
    )
    sort = models.IntegerField(default=1, verbose_name="显示排序", help_text="显示排序")
    STATUS_CHOICES = (("0", "正常"), ("1", "停用"))
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default="0",
        verbose_name="状态（0正常 1停用）",
        help_text="状态（0正常 1停用）",
    )
    remark = models.CharField(max_length=255, null=True, blank=True, verbose_name="备注", help_text="备注")

    class Meta:
        db_table = "app_nurse_dept"
        verbose_name = "长护师-部门"
        verbose_name_plural = verbose_name
        ordering = ("sort", "-create_datetime")

    def __str__(self):
        return self.dept_name