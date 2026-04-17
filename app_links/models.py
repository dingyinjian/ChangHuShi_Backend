# app_links/models.py
from django.db import models
from app_user.models import Users

class Link(models.Model):
    CATEGORY_CHOICES = [
        ('1', '开发'),
        ('2', '设计'),
        ('9', '其他'),
    ]
    title = models.CharField(max_length=200, verbose_name="标题")
    url = models.URLField(verbose_name="链接地址")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='1', verbose_name="分类")
    description = models.TextField(blank=True, null=True, verbose_name="备注/描述")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")  # True=启用，False=停用
    #CASCADE=级联删除，当关联的对象（如 Users 实例）被删除时，自动删除所有引用它的对象（比如这个 owner 所属的记录也会被删）。
    #PROTECT=保护模式，阻止删除关联对象。如果尝试删除被引用的 Users 实例，Django 会抛出 ProtectedError 异常。
    #SET_NULL=设为 NULL，当关联对象被删除时，将外键字段设为 NULL。前提是该字段必须允许为空（即 null=True），使用软删除、保留历史记录但解除关联。
    #SET_DEFAULT=设为默认值，删除关联对象时，外键字段设为默认值。字段必须有 default=... 设置。
    #models.SET(value) 或 models.SET(callable)。自定义设置值。调用一个函数或直接指定一个值来设置外键。常见用法：设置“哨兵对象”（sentinel object），比如一个专门表示“已删除用户”的虚拟用户。
    #DO_NOTHING=不做任何操作。Django 不采取任何措施，但数据库可能会报错（如果数据库启用了外键约束）。可能导致数据库完整性错误（如 PostgreSQL/MySQL 会拒绝删除）。适用场景：极少数情况，比如你手动管理外键，或使用无外键约束的数据库（如 SQLite 开发环境）。
    owner = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="所有者")
    # 存储图片 URL 列表（JSON 字符串）
    image_urls = models.TextField(
        blank=True,
        default='[]',
        verbose_name="封面图 URL 列表"
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="最后更新")
    class Meta:
        verbose_name = "收藏链接"
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return self.title
