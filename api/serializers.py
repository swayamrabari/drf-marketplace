from rest_framework import serializers  # noqa: I001
from .models import Category, Product, Order, OrderItem
from .services import create_order


class CategoryBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ProductBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'stock')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')

    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                'Category name must be at least 3 characters long.'
            )
        return value

    def validate_description(self, value):
        if value and len(value.split()) < 2:
            raise serializers.ValidationError(
                'Category description must be at least 2 words long.'
            )
        return value


class CategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductBasicSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'products')


class ProductSerializer(serializers.ModelSerializer):
    category = CategoryBasicSerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, source='category'
    )

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'category_id',
            'name',
            'description',
            'price',
            'stock',
            'created_at',
        )

    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                'Product name must be at least 3 characters long.'
            )
        return value

    def validate_description(self, value):
        if value and len(value.split()) < 2:
            raise serializers.ValidationError(
                'Product description must be at least 2 words long.'
            )
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Product price must be a positive number.'
            )
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('Product stock cannot be negative.')
        return value


class OrderSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True,
        source='product',
    )

    quantity = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'product_id',
            'quantity',
            'total_amount',
            'status',
            'created_at',
        )

        read_only_fields = ('user', 'total_amount', 'status', 'created_at')

    def create(self, validated_data):
        product = validated_data.pop('product')
        quantity = validated_data.pop('quantity')

        return create_order(
            user=self.context['request'].user, product=product, quantity=quantity
        )
