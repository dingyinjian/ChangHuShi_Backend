from django.db import migrations


def forwards(apps, schema_editor):
    Menu = apps.get_model("app_menu", "Menu")
    Menu.objects.filter(path__in=["sop", "/sop"], menu_type="C").update(parent=None)


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("app_sop", "0003_normalize_sop_menu_i18n"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
