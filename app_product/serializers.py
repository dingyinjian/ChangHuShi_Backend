from rest_framework import serializers
from app_product.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'is_active', 'sort_order', 'created_at']

class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'is_active', 'sort_order']


class ProductSerializer(serializers.ModelSerializer):
    """用于list列表 / retrieve和详情"""
    category_name=serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'category_name', 'product_id','price', 'original_price', 'stock', 'is_active','delivery_type', 'description', 'sort_order','created_at', 'updated_at']
        read_only_fields = ['id','created_at', 'updated_at']

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields=['name', 'category', 'product_id','price', 'original_price', 'stock', 'is_active','delivery_type', 'description', 'sort_order']
    #自定义字段校验方法确保 product_id 字段在整个系统中是唯一的，但允许在更新商品时不报错（排除自己）。
    #DRF 约定：validate_字段名 方法是针对特定字段的自定义验证
    # 调用时机：在序列化器验证 product_id 字段时自动调用
    # 参数：value 是前端传来的 product_id 值
    # 返回值：验证通过后返回的值（可以修改）
    def validate_product_id(self, value):
        if value:
            queryset=Product.objects.filter(product_id=value)
            if self.instance:
                queryset=queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError("商品ID已存在")
        return value
