from django.db import models
from .category import Category
from .edition import Edition


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=999)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='', null=True, blank=True)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, default='', null=True, blank=True)
    description = models.CharField(max_length=200, default='', null=True, blank=True)
    image = models.ImageField(upload_to='uploads/products/')

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in = ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()

    @staticmethod
    def get_all_products_by_editionid(edition_id):
        if edition_id:
            return Product.objects.filter(edition=edition_id)
        else:
            return Product.get_all_products()
