from django.db import migrations


def seed_sop_menu(apps, schema_editor):
    Menu = apps.get_model("app_menu", "Menu")

    # 顶级菜单：与首页同级（parent 为空）
    # 菜单名称需与前端 i18n 键一致（侧边栏使用 $t(meta.title)）
    sop_menu, _ = Menu.objects.get_or_create(
        path="/sop",
        menu_type="C",
        defaults={
            "parent": None,
            "menu_name": "message.router.systemSop",
            "icon": "iconfont icon-zujian",
            "sort": 90,
            "component": "system/sop/index",
            "is_iframe": "1",
            "is_link": "",
            "is_hide": "0",
            "is_keep_alive": "0",
            "is_affix": "1",
            "permission": "system:sop:list",
            "status": "0",
            "remark": "SOP管理菜单",
        },
    )

    button_defs = [
        ("新增", "system:sop:add", 1),
        ("编辑", "system:sop:edit", 2),
        ("删除", "system:sop:delete", 3),
        ("上传", "system:sop:upload", 4),
    ]
    for name, perm, sort in button_defs:
        Menu.objects.get_or_create(
            parent=sop_menu,
            menu_name=name,
            menu_type="F",
            defaults={
                "sort": sort,
                "is_hide": "0",
                "is_keep_alive": "1",
                "is_affix": "1",
                "permission": perm,
                "status": "0",
                "remark": f"SOP{name}按钮",
            },
        )


def rollback_sop_menu(apps, schema_editor):
    Menu = apps.get_model("app_menu", "Menu")
    menu = Menu.objects.filter(path__in=["/sop", "sop"], menu_type="C").first()
    if menu:
        Menu.objects.filter(parent=menu).delete()
        menu.delete()


class Migration(migrations.Migration):
    dependencies = [
        ("app_menu", "0002_initial"),
        ("app_sop", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_sop_menu, rollback_sop_menu),
    ]

