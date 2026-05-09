from django.db import migrations


def forwards(apps, schema_editor):
    Menu = apps.get_model("app_menu", "Menu")
    Menu.objects.filter(path__in=["sop", "/sop"], menu_type="C").update(
        menu_name="message.router.systemSop",
        is_keep_alive="0",
    )


def backwards(apps, schema_editor):
    Menu = apps.get_model("app_menu", "Menu")
    Menu.objects.filter(path__in=["sop", "/sop"], menu_type="C", menu_name="message.router.systemSop").update(
        menu_name="SOP管理",
        is_keep_alive="1",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("app_sop", "0002_seed_sop_menu"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
