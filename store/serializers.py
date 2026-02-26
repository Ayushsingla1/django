from rest_framework import serializers
from store.models import Product, Collection, Review
from decimal import Decimal

class CollectionSerialer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id','title','product_count']

    product_count = serializers.IntegerField(read_only = True)

# name of the field dont need to match exactly
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id','title','price','price_with_tax','collections']

    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length = 255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2)
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # # collections = serializers.StringRelatedField()
    # # collections = CollectionSerialer()
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(),
    #     view_name = 'collection-detail',
    #     source = "collections"
    # )


    def calculate_tax(self, product : Product):
        return Decimal(1.1) * product.price

    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.inventory = 100
    #     product.save()
    #     return product

    # def update(self, instance, validated_data):
    #     instance.price = validated_data.get("price")
    #     instance.save()
    #     return instance


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'name', 'review', 'date']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id = product_id, **validated_data)
    