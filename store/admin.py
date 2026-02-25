from django.contrib import admin
from . import models
from django.db.models import Count, Func, F
from django.urls import reverse
from django.utils.html import format_html, urlencode
# Register your models here.

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    list_display = ['title','price','inventory_status','collection_status']
    list_per_page = 10
    list_editable = ['price']
    list_select_related = ['collections']

    def collection_status(self,product):
        return product.collections.title

    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory < 10:
            return "Low"
        return "Ok"
    
    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        update_count = queryset.update(inventory = 0)
        self.message_user(
            request,
            f'{update_count} products were succesfully cleared'
        )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','orders']
    # list_select_related = ['order']

    def orders(self,customer):
        items = []
        for order in customer.order_set.all():
            print(order.placed_at)
            for mapping in order.productordermapping_set.select_related('products').all():
                print(mapping.products)
                items.append(mapping.products)
        return items

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('order_set','order_set__productordermapping_set__products')



@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','product_count']

    @admin.display(ordering='product_count')
    def product_count(self,collection):
        url = ( reverse("admin:store_product_changelist")
               + '?'
               + urlencode({
                   'collections__id' : collection.id
               })
               )
        return format_html("<a href = {}>{}</a>",url,collection.product_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count = Count('product')
        )

# admin.site.register(models.Product)