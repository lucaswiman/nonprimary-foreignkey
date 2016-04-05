from django.test.testcases import TestCase
from nonprimary_foreignkey.tests.models import Item
from nonprimary_foreignkey.tests.models import ReceivedItem


class TestGet(TestCase):
    def setUp(self):
        Item.objects.all().delete()
        self.barcode = '12345'
        self.item = Item.objects.create(barcode=self.barcode)

    def test_get(self):
        from_instance = ReceivedItem.objects.create()
        from_instance.barcode = self.barcode
        self.assertEqual(from_instance.item, self.item)

    def test_get_non_existent_barcode(self):
        from_instance = ReceivedItem.objects.create()
        from_instance.barcode = 'not a barcode'
        with self.assertRaises(Item.DoesNotExist):
            from_instance.item

    def test_get_multiple_objects(self):
        Item.objects.create(barcode=self.barcode)
        from_instance = ReceivedItem.objects.create()
        from_instance.barcode = self.barcode
        with self.assertRaises(Item.MultipleObjectsReturned):
            from_instance.item


class TestSet(TestCase):
    def setUp(self):
        Item.objects.all().delete()
        self.barcode = '12345'
        self.item = Item.objects.create(barcode=self.barcode)

    def test_set(self):
        from_instance = ReceivedItem.objects.create()
        from_instance.item = self.item
        self.assertEqual(from_instance.item, self.item)
        self.assertEqual(from_instance.barcode, self.barcode)

    def test_set_null(self):
        from_instance = ReceivedItem.objects.create()
        from_instance.item = self.item
        self.assertEqual(from_instance.item, self.item)
        self.assertEqual(from_instance.barcode, self.barcode)
        from_instance.item = None
        self.assertEqual(from_instance.item, None)
        self.assertEqual(from_instance.barcode, None)

    def test_set_underlying_field_null(self):
        from_instance = ReceivedItem.objects.create()
        self.assertEqual(from_instance.barcode, None)
        self.assertEqual(from_instance.item, None)
