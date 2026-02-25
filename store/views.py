from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer, CollectionSerialer
from rest_framework import status
from django.shortcuts import get_list_or_404
# from django.db.models import FieldDoesNotExist
# Create your views here.

@api_view()
def product_list(request):

    query_set = Product.objects.select_related('collections').all()
    serialized_products = ProductSerializer(query_set, many = True, context = {'request' : request}).data
    return Response(serialized_products)

@api_view()
def product_details(request, id):
    
    # try:
    #     product = Product.objects.get(pk = id)
    #     serialized_product = ProductSerializer(product).data
    #     return Response(serialized_product)
    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)

    product = get_list_or_404(Product, pk = id)
    serialized_product = ProductSerializer(product).data
    return Response(serialized_product)


@api_view()
def collection_details(request, pk):

    collection = get_list_or_404(Product, pk = pk)
    serialied_collection = CollectionSerialer(collection).data
    return Response(serialied_collection)