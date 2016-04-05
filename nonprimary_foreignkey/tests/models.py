from django.db import models

from nonprimary_foreignkey.fields import NonPrimaryForeignKey


class Item(models.Model):
    barcode = models.CharField(null=False, max_length=100)

    def __repr__(self):
        return 'Item(barcode=%r)' % self.barcode


class ReceivedItem(models.Model):
    barcode = models.CharField(null=True, max_length=100)
    item = NonPrimaryForeignKey('tests.Item', 'barcode', 'barcode')
