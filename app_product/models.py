from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField('分类名称',max_length=100,unique=True)
    slug=models.SlugField('URL标识',unique=True,max_length=100,blank=True,help_text='用于URL')
    description=models.TextField('描述',blank=True,null=True)
    is_active=models.BooleanField('是否启用',default=True)
    sort_order=models.PositiveSmallIntegerField('排序',default=0)
    created_at=models.DateTimeField('创建时间',auto_now_add=True)
    updated_at=models.DateTimeField('更新时间',auto_now=True)
    class Meta:
        verbose_name='商品分类'
        verbose_name_plural=verbose_name
        ordering=['sort_order','name']
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class Product(models.Model):
    DELEVERY_TYPE_CHOICES = [('auto','自动发卡'),('manual','手动发货')]
    name=models.CharField('商品名称',max_length=100)
    category=models.ForeignKey(Category,on_delete=models.PROTECT,verbose_name='所属分类')
    # unique保持唯一性 唯一约束
    # blank=True 表单验证时允许为空（注意：这是 Django 表单/DRF 层面的行为，不是数据库！）
    # 你的字段定义中 没有写 null=True，所以
    # 数据库列：NOT NULL（不能为空）
    # 但 Django 允许你在保存前不传值（只要最终存入非空字符串即可）
    product_id=models.CharField('商品ID',max_length=100,unique=True,blank=True)
    # 整数部分最大位数10位，小数部分最大位数2位
    price=models.DecimalField('售价',max_digits=10,decimal_places=2,default=0)
    original_price=models.DecimalField('原价',max_digits=10,decimal_places=2,default=0,null=True,blank=True)
    # 库存默认值为0,PositiveIntegerField非负整数
    stock=models.PositiveIntegerField('库存',default=0)
    is_active=models.BooleanField('上架状态',default=True)
    delivery_type=models.CharField('发货方式',max_length=10, choices=DELEVERY_TYPE_CHOICES,default='auto')
    description=models.TextField('商品描述',blank=True,null=True)
    sort_order=models.PositiveSmallIntegerField('排序',default=0)
    created_at=models.DateTimeField('创建时间',auto_now_add=True)
    updated_at=models.DateTimeField('更新时间',auto_now=True)
    class Meta:
        verbose_name='商品'
        verbose_name_plural=verbose_name
        ordering=['sort_order','-created_at']
    def __str__(self):
        return self.name