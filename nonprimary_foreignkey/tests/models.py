from django.db import models

from nonprimary_foreignkey.fields import NonPrimaryForeignKey


class Item(models.Model):
    barcode = models.CharField(null=False, max_length=100)


class ReceivedItem(models.Model):
    barcode = models.CharField(null=True, max_length=100)
    item = NonPrimaryForeignKey('tests.Item', 'barcode', 'barcode')
