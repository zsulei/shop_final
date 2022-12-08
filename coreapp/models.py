from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class Client(AbstractUser):
    username = models.EmailField(unique=True, null=True, )
    avatar = models.ImageField(default='avatars/default.svg', upload_to='avatars/')
    first_name = models.CharField(max_length=50, blank=False, )
    last_name = models.CharField(max_length=50, )
    is_staff = models.BooleanField(default=False, )
    activation_code = models.CharField(max_length=17, blank=True, null=True, )
    date_joined = models.DateTimeField(auto_now_add=True, )

    def __str__(self):
        if self.username:
            return self.username
        else:
            return self.first_name

    class Meta:
        ordering = ('first_name', 'last_name', 'username', )
        permissions = [('can_buy_products', 'this permission for simple buyers only')]


class Product(models.Model):
    title = models.CharField(max_length=100, )
    color = models.CharField(max_length=30, )
    image = models.ImageField(upload_to='products', default='products/default.svg')
    description = models.TextField(null=True)
    is_popular = models.BooleanField(default=False, )
    price = models.FloatField()
    category = models.ForeignKey('Categories', on_delete=models.SET_NULL, blank=True, null=True, )
    product_type = models.ForeignKey('Type', on_delete=models.SET_NULL, blank=True, null=True, )
    material = models.ForeignKey('Material', on_delete=models.SET_NULL, blank=True, null=True, )
    size = models.ManyToManyField('Size', )
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.SET_NULL, blank=True, null=True, )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('coreapp/home.html', args=[str(self.id)], )


class Categories(models.Model):
    category = models.CharField(max_length=50, )

    def __str__(self):
        return self.category


class Material(models.Model):
    material = models.CharField(max_length=20, )

    def __str__(self):
        return self.material


class Size(models.Model):
    size = models.CharField(max_length=10, )

    def __str__(self):
        return str(self.size)


class Type(models.Model):
    product_type = models.CharField(max_length=30, )

    def __str__(self):
        return self.product_type


class Manufacturer(models.Model):
    country = models.CharField(max_length=100, )

    def __str__(self):
        return self.country


class Purchase(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product}-{self.quantity}'


class AdminLog(models.Model):
    purchase = models.ManyToManyField('Purchase', )
    client = models.ForeignKey('Client', on_delete=models.CASCADE, )
    purchase_date = models.DateTimeField(auto_now=False, auto_now_add=False, )
    total_price = models.FloatField()

    def __str__(self):
        return str(self.purchase_date)
