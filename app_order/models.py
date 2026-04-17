
from django.db import models
from app_user.models import Users


# Create your models here.
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('delivered', '已发货(卡密已发放)'),
        ('cancelled', '已取消'),
        ('refunded', '已退款'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('alipay','支付宝'),
        ('wechat','微信支付'),
        ('other','其它')
    ]
    # unique=True,唯一约束  db_index=True 数据库索引
    order_no = models.CharField('订单号',max_length=32, unique=True,db_index=True)
    # CASCADE=级联删除，当关联的对象（如 Users 实例）被删除时，自动删除所有引用它的对象（比如这个 owner 所属的记录也会被删）。例如：删除用户A → 用户A的所有订单自动删除
    # PROTECT=保护模式，阻止删除关联对象。如果尝试删除被引用的 Users 实例，Django 会抛出 ProtectedError 异常。
    # SET_NULL=设为 NULL，当关联对象被删除时，将外键字段设为 NULL。前提是该字段必须允许为空（即 null=True），使用软删除、保留历史记录但解除关联。
    # SET_DEFAULT=设为默认值，删除关联对象时，外键字段设为默认值。字段必须有 default=... 设置。
    # models.SET(value) 或 models.SET(callable)。自定义设置值。调用一个函数或直接指定一个值来设置外键。常见用法：设置“哨兵对象”（sentinel object），比如一个专门表示“已删除用户”的虚拟用户。
    # DO_NOTHING=不做任何操作。Django 不采取任何措施，但数据库可能会报错（如果数据库启用了外键约束）。可能导致数据库完整性错误（如 PostgreSQL/MySQL 会拒绝删除）。适用场景：极少数情况，比如你手动管理外键，或使用无外键约束的数据库（如 SQLite 开发环境）。
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="用户")
    # product=models.ForeignKey(Product,on_delete=models.PROTECT,verbose_name='商品')