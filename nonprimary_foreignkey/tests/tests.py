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


class TestPrefetch(TestCase):
    def setUp(self):
        Item.objects.all().delete()
        self.barcode1 = '12345'
        self.item1 = Item.objects.create(barcode=self.barcode1)
        self.barcode2 = '67890'
        self.item2 = Item.objects.create(barcode=self.barcode2)

    def test_constant_queries(self):
        self.assertEqual(
            ReceivedItem.objects.create(barcode=self.barcode1).item,
            self.item1)
        self.assertEqual(
            ReceivedItem.objects.create(barcode=self.barcode2).item,
            self.item2)
        with self.assertNumQueries(1):
            self.assertEqual(len(ReceivedItem.objects.all()), 2)
        # Prefetching should include the query to grab the related ``Item`` objects.
        with self.assertNumQueries(2):
            queryset = ReceivedItem.objects.prefetch_related('item')
            self.assertEqual(len(queryset), 2)
        with self.assertNumQueries(0):
            self.assertEqual({obj.item for obj in queryset}, {self.item1, self.item2})

    def test_null(self):
        self.assertEqual(
            ReceivedItem.objects.create(barcode=None).item,
            None)
        self.assertEqual(
            ReceivedItem.objects.create(barcode=self.barcode1).item,
            self.item1)
        with self.assertNumQueries(2):
            queryset = ReceivedItem.objects.prefetch_related('item')
            self.assertEqual(len(queryset), 2)
        with self.assertNumQueries(0):
            self.assertEqual({obj.item for obj in queryset}, {self.item1, None})
