from django.db import migrations


def forwards(apps, schema_editor):
    Menu = apps.get_model("app_menu", "Menu")
    # 顶级 path 必须为 /sop，否则前端拼接会得到 //sop 导致 404
    Menu.objects.filter(path="sop", menu_type="C").update(path="/sop")


def backwards(apps, schema_editor):
    Menu = apps.get_model("app_menu", "Menu")
    Menu.objects.filter(path="/sop", menu_type="C").update(path="sop")


class Migration(migrations.Migration):
    dependencies = [
        ("app_sop", "0004_sop_menu_top_level"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
