from __future__ import unicode_literals

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class Post(models.Model):
    name = models.CharField(max_length=250)
    vendor = models.CharField(max_length=50)
    image = models.TextField()
    description = models.TextField()
    slug = models.TextField()
    category = models.ManyToManyField(Category,  related_name='catalog')

    def __unicode__(self):
        return self.name