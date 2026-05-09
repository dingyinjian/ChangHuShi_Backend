# Generated manually for Task model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app_nurse", "0001_initial"),
        ("app_service_object", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id", utils.models.SnowflakeIDField(primary_key=True, serialize=False)),
                ("modifier", models.CharField(blank=True, help_text="修改人", max_length=255, null=True, verbose_name="修改人")),
                ("update_datetime", models.DateTimeField(auto_now=True, null=True, verbose_name="更新时间")),
                ("create_datetime", models.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")),
                ("task_name", models.CharField(help_text="任务名称", max_length=255, verbose_name="任务名称")),
                ("start_time", models.DateTimeField(help_text="开始时间", verbose_name="开始时间")),
                ("end_time", models.DateTimeField(help_text="结束时间", verbose_name="结束时间")),
                ("service_report", models.TextField(blank=True, help_text="服务报告", null=True, verbose_name="服务报告")),
                ("service_score", models.DecimalField(blank=True, decimal_places=2, help_text="服务分数", max_digits=5, null=True, verbose_name="服务分数")),
                ("report_status", models.CharField(choices=[("pending", "待报告"), ("done", "已回写")], default="pending", help_text="报告状态", max_length=16, verbose_name="报告状态")),
                ("creator", models.ForeignKey(db_constraint=False, help_text="创建人", null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name="creator_query", to=settings.AUTH_USER_MODEL, verbose_name="创建人")),
                ("owner", models.ForeignKey(db_constraint=False, help_text="负责人（长护师）", on_delete=django.db.models.deletion.PROTECT, related_name="tasks", to="app_nurse.nurse", verbose_name="负责人")),
                ("service_object", models.ForeignKey(db_constraint=False, help_text="被服务对象", on_delete=django.db.models.deletion.PROTECT, related_name="tasks", to="app_service_object.serviceobject", verbose_name="被服务对象")),
            ],
            options={
                "verbose_name": "任务管理",
                "verbose_name_plural": "任务管理",
                "db_table": "app_task",
                "ordering": ("-update_datetime",),
            },
        ),
    ]
