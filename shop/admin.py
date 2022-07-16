from django.contrib import admin
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order
from .models.edition import Edition

class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'edition']

class AdminCategory(admin.ModelAdmin):
    list_display = ['name']

class AdminEdition(admin.ModelAdmin):
    list_display = ['name']

class AdminCustomer(admin.ModelAdmin):
    list_display = ['first_name', 'email']


# Register your models here.

admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategory)
admin.site.register(Customer, AdminCustomer)
admin.site.register(Order)
admin.site.register(Edition)

