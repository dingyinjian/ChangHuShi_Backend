from django.db import models

from utils.models import BaseModel


class Task(BaseModel):
    """长护任务（负责人、服务对象、时间与报告）"""

    REPORT_STATUS_CHOICES = (
        ("pending", "待报告"),
        ("done", "已回写"),
    )

    task_name = models.CharField(max_length=255, verbose_name="任务名称", help_text="任务名称")
    owner = models.ForeignKey(
        "app_nurse.Nurse",
        on_delete=models.PROTECT,
        db_constraint=False,
        related_name="tasks",
        verbose_name="负责人",
        help_text="负责人（长护师）",
    )
    service_object = models.ForeignKey(
        "app_service_object.ServiceObject",
        on_delete=models.PROTECT,
        db_constraint=False,
        related_name="tasks",
        verbose_name="被服务对象",
        help_text="被服务对象",
    )
    start_time = models.DateTimeField(verbose_name="开始时间", help_text="开始时间")
    end_time = models.DateTimeField(verbose_name="结束时间", help_text="结束时间")
    service_report = models.TextField(
        verbose_name="服务报告",
        help_text="服务报告",
        null=True,
        blank=True,
    )
    service_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="服务分数",
        help_text="服务分数",
        null=True,
        blank=True,
    )
    report_status = models.CharField(
        max_length=16,
        choices=REPORT_STATUS_CHOICES,
        default="pending",
        verbose_name="报告状态",
        help_text="报告状态",
    )
    sop_items = models.ManyToManyField(
        "app_sop.Sop",
        blank=True,
        related_name="tasks",
        verbose_name="护理项目",
        help_text="关联 SOP（护理项目），可多选",
    )

    class Meta:
        db_table = "app_task"
        verbose_name = "任务管理"
        verbose_name_plural = verbose_name
        ordering = ("-update_datetime",)

    def __str__(self):
        return self.task_name
