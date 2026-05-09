from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_sop", "0001_initial"),
        ("app_task", "0002_seed_task_menu"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="sop_items",
            field=models.ManyToManyField(
                blank=True,
                help_text="关联 SOP（护理项目），可多选",
                related_name="tasks",
                to="app_sop.sop",
                verbose_name="护理项目",
            ),
        ),
    ]
