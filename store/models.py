from django.db import models

# Create your models here.
#


class Collection(models.Model):

    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']


class Product(models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    collections = models.ForeignKey(Collection, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Customer(models.Model):

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(unique=True)
    phone = models.CharField(max_length=10)
    birth_date = models.DateField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['email'])
        ]


class Order(models.Model):

    ORDER_PAYMENT_STATUS = [("P", "Pending"), ("C", "Completed"), ("F", "Failed")]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=ORDER_PAYMENT_STATUS)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.placed_at)


class Address(models.Model):

    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    customer = models.OneToOneField(
        Customer, primary_key=True, on_delete=models.CASCADE
    )  # one to one relationship
    # customer = models.ForeignKey(
    #     Customer, on_delete=models.CASCADE
    # ) # one to many relationship
    class Meta:
        indexes = [
            models.Index(fields=['city'])
        ]


class ProductOrderMapping(models.Model):
    orders = models.ForeignKey(Order, on_delete=models.PROTECT)
    products = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItems(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
