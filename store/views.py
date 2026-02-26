from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Collection, ProductOrderMapping, Review
from .serializers import ProductSerializer, CollectionSerialer, ReviewSerializer
from rest_framework import status
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Count
from rest_framework.views import APIView
# from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
# from django.db.models import FieldDoesNotExist
# Create your views here.

class ProductViewSet(ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['collections_id']

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collections_id = collection_id)
        
    #     return queryset

    def get_serializer_context(self):
        return {'request' : self.request}
    
    def destroy(self, request, *args, **kwargs):
        if  ProductOrderMapping.objects.filter(products_id = kwargs['pk']).count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        return super().destroy(request, *args, **kwargs)

    # def delete(self, request, id):
    #     product = get_object_or_404(Product, pk = id)
    #     if product.productordermapping_set.count() > 0:
    #         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT) 

# class ProductList(ListCreateAPIView):
    # queryset = Product.objects.all()
    # serializer_class = ProductSerializer

    # def get_queryset(self):
    #     return Product.objects.select_related('collections').all()
    
    # def get_serializer_class(self):
    #     return ProductSerializer
    
    # def get_serializer_context(self):
    #     return {'request' : self.request} 
    
    # def get(self, request):
    #     query_set = Product.objects.select_related('collections').all() 
    #     serialized_products = ProductSerializer(query_set, many = True, context = {'request' : request}).data
    #     return Response(serialized_products)
    
    # def post(self, request):
    #     serializer = ProductSerializer(data = request.data)
    #     serializer.is_valid(raise_exception = True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    

# class ProductDetails(RetrieveUpdateDestroyAPIView):

    


# class ProductDetails(APIView):

#     # def __init__(self): 

#     def get(self, request, id):
#         query_set = get_object_or_404(Product, pk = id)
#         serialized_product = ProductSerializer(query_set).data
#         return Response(serialized_product)
    
#     def put(self, request, id):
#         product = get_object_or_404(Product, pk = id)
#         serializer = ProductSerializer(product, data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk = id)
#         if product.productordermapping_set.count() > 0:
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        
        

# @api_view()
# def collection_details(request, pk):

#     collection = Collection.objects.annotate(product_count = Count('product')).all()
#     serialied_collection = CollectionSerialer(collection).data
#     return Response(serialied_collection)
    
# class CollectionDetails(ListCreateAPIView):

#     queryset = Collection.objects.annotate(product_count = Count('product')).all()
#     serializer_class = CollectionSerialer


class CollectionViewSet(ModelViewSet):

    queryset = Collection.objects.annotate(product_count = Count('product')).all()
    serializer_class = CollectionSerialer 


class ReviewViewSet(ModelViewSet):

    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id' : self.kwargs['product_pk']}