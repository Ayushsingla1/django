from django.shortcuts import render
from store.models import Product, ProductOrderMapping
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F
# Create your views here.
# here we write requestHandler

def say_hello(request):

    product = Product.objects.filter(pk = 0).first()
    print(product)

    # try:
    #   product = Product.objects.get(pk = 0) 
    # except ObjectDoesNotExist:
    #   pass


    # to get products where inventory < 20 | price < 10
    # product = Product.objects.filter(Q(inventory__lt = 20) | Q(price__lt = 10))

    # to get product where inventory = price
    # product = Product.objects.filter(inventory = F('price'))

    # query = Product.objects.values('id', 'title', 'collection__title')

    # query = Product.objects.filter(id__in = ProductOrderMapping.objects.values('products_id').distinct()).order_by('title')

    # select_related(1) ->  (1 to 1 mapping like thing) or  (n to 1 mapping)
    # prefetch_related(n) -> 1 to n mapping
    return render(request, "index.html")
