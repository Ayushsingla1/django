from rest_framework import serializers
from store.models import Product, Collection
from decimal import Decimal

class CollectionSerialer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)

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
