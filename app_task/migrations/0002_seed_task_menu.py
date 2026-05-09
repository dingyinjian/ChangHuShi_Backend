from django.db import migrations


def seed_task_menu(apps, schema_editor):
    Menu = apps.get_model("app_menu", "Menu")

    task_menu, _ = Menu.objects.get_or_create(
        path="/task",
        menu_type="C",
        defaults={
            "parent": None,
            "menu_name": "message.router.systemTask",
            "icon": "iconfont icon-zujian",
            "sort": 88,
            "component": "system/task/index",
            "is_iframe": "1",
            "is_link": "",
            "is_hide": "0",
            "is_keep_alive": "0",
            "is_affix": "1",
            "permission": "system:task:list",
            "status": "0",
            "remark": "任务管理菜单",
        },
    )

    button_defs = [
        ("新增", "system:task:add", 1),
        ("编辑", "system:task:edit", 2),
        ("删除", "system:task:delete", 3),
        ("查看报告", "system:task:view_report", 4),
        ("回写报告", "system:task:apply_report", 5),
    ]
    for name, perm, sort in button_defs:
        Menu.objects.get_or_create(
            parent=task_menu,
            menu_name=name,
            menu_type="F",
            defaults={
                "sort": sort,
                "is_hide": "0",
                "is_keep_alive": "1",
                "is_affix": "1",
                "permission": perm,
                "status": "0",
                "remark": f"任务{name}按钮",
            },
        )


def rollback_task_menu(apps, schema_editor):
    Menu = apps.get_model("app_menu", "Menu")
    menu = Menu.objects.filter(path__in=["/task", "task"], menu_type="C").first()
    if menu:
        Menu.objects.filter(parent=menu).delete()
        menu.delete()


class Migration(migrations.Migration):
    dependencies = [
        ("app_menu", "0002_initial"),
        ("app_task", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_task_menu, rollback_task_menu),
    ]
