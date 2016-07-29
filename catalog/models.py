from __future__ import unicode_literals

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=250)
    sku = models.CharField(max_length=30)
    vendor = models.CharField(max_length=50)
    image = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    oldprice = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    description = models.TextField()
    slug = models.TextField()
    category = models.ManyToManyField(Category,  related_name='catalog')

    def __unicode__(self):
        return self.name