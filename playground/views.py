from django.shortcuts import render
from store.models import Product, ProductOrderMapping, Collection, Order
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Count, Func, Value, ExpressionWrapper, DecimalField
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem
from django.db import transaction

# Create your views here.
# here we write requestHandler
# @transaction.atomic
def say_hello(request):

    # product = Product.objects.filter(pk = 0).first()
    # print(product)

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

    # counts total number of products in the products table
    # counts_product = Product.objects.aggregate(count = Count('id'))

    # counts total number of products in the products table and also returns the minimum of the price
    # counts_product = Product.objects.aggregate(count = Count('id'), min_price = Min('price'))  

    # full_name = Product.objects.annotate(
    #     full_name = Func(
    #         F('first_name'), Value(' '), F('last_name'), 
    #         function = 'CONCAT')
    #     )

    # this wont work as price is a decimal type wherease 0.8 is float type
    # discounted_price = Product.objects.annotate(discounted_price = F('price') * 0.8)

    # this is how it works

    # discounted_price = ExpressionWrapper(F('price') * 0.8, output_field=DecimalField())
    # query_state = Product.objects.annotate(
    #     discounted_price = discounted_price
    # )

    # 
    
    # content_type = ContentType.objects.get_for_model(Product)

    # query = TaggedItem.objects.select_related('tag').filter(
    #     content_type = content_type,
    #     object_id = 1
    # )

    # query = TaggedItem.objects.get_tags_for(Product,1)

    ###### creating a object
    # collection = Collection()
    # collection.title = 'Something good'
    # collection.save()

    ##### updating a object
    # Collection.objects.filter(pk=1).update(title = 'protein')

    ###### for deleting a single object
    # collection = Collection(pk = 1)
    # collection.delete()

    ###### for deleting multiple objects at once
    # collection = Product.objects.filter(id_gt = 5).delete()

    ##### atomic transaction

    with transaction.atomic():
        order = Order()
        order.customer_id = 2
        order.save()

        orderItem = ProductOrderMapping()
        orderItem.quantity = 5
        orderItem.products_id = 1
        orderItem.unit_price = 10
        orderItem.orders = order
        orderItem.save()

    return render(request, "index.html")
