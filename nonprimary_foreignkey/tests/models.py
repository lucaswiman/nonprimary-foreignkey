from django.db import models

from nonprimary_foreignkey.fields import NonPrimaryForeignKey


class ItemType(models.Model):
    pass


class Item(models.Model):
    barcode = models.CharField(null=False, max_length=100)
    item_type = models.ForeignKey(ItemType, null=True, default=None)

    def __repr__(self):
        return 'Item(barcode=%r)' % self.barcode


class ReceivedItem(models.Model):
    barcode = models.CharField(null=True, max_length=100)
    item = NonPrimaryForeignKey('tests.Item', 'barcode', 'barcode')


class RelatedItem(models.Model):
    item = models.ForeignKey(Item)
