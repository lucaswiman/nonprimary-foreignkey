from django.db.models import Prefetch
from django.test.testcases import TestCase
from mock import patch

from nonprimary_foreignkey.tests.models import Item
from nonprimary_foreignkey.tests.models import ItemType
from nonprimary_foreignkey.tests.models import ReceivedItem


class TestGet(TestCase):
    def setUp(self):
        Item.objects.all().delete()
        self.barcode = '12345'
        self.item = Item.objects.create(barcode=self.barcode)
        self.barcode2 = '67890'
        self.item2 = Item.objects.create(barcode=self.barcode2)

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

    def test_get_underlying_field_null(self):
        from_instance = ReceivedItem.objects.create()
        self.assertEqual(from_instance.barcode, None)
        self.assertEqual(from_instance.item, None)

    def test_get_cache_behavior(self):
        from_instance = ReceivedItem.objects.create()
        from_instance.barcode = self.barcode
        with self.assertNumQueries(1):
            self.assertEqual(from_instance.item, self.item)
        with self.assertNumQueries(0):
            self.assertEqual(from_instance.item, self.item)

        # Invalidate the cache by setting the underlying field.
        from_instance.barcode = self.barcode2
        with self.assertNumQueries(1):
            self.assertEqual(from_instance.item, self.item2)


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

    def test_wrong_type(self):
        from_instance = ReceivedItem.objects.create()
        self.assertEqual(from_instance.barcode, None)
        with self.assertRaises(TypeError):
            from_instance.item = object()


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

    def test_set_underlying_field_with_prefetched_object(self):
        self.assertEqual(
            ReceivedItem.objects.create(barcode=self.barcode1).item,
            self.item1)
        [item] = ReceivedItem.objects.prefetch_related('item').all()
        with self.assertNumQueries(0):
            self.assertEqual(item.item, self.item1)
        with self.assertNumQueries(1):
            item.barcode = self.item2.barcode
            self.assertEqual(item.item, self.item2)

    def test_set_with_prefetched_object(self):
        self.assertEqual(
            ReceivedItem.objects.create(barcode=self.barcode1).item,
            self.item1)
        [item] = ReceivedItem.objects.prefetch_related('item')
        with self.assertNumQueries(0):
            self.assertEqual(item.item, self.item1)
        item.item = self.item2
        with self.assertNumQueries(0):
            self.assertEqual(item.item, self.item2)

    def test_prefetch_custom_queryset(self):
        self.item1.item_type = ItemType.objects.create()
        self.item1.save()
        self.assertEqual(
            ReceivedItem.objects.create(barcode=self.barcode1).item,
            self.item1)
        with self.assertNumQueries(2):
            [item] = ReceivedItem.objects.prefetch_related(
                Prefetch('item', queryset=Item.objects.select_related('item_type')))
        with self.assertNumQueries(0):
            self.assertEqual(item.item.item_type, self.item1.item_type)

    def test_prefetch_multiple_levels(self):
        self.item1.relateditem_set.create()
        self.item1.relateditem_set.create()
        self.item1.relateditem_set.create()
        self.assertEqual(
            ReceivedItem.objects.create(barcode=self.barcode1).item,
            self.item1)
        with self.assertNumQueries(3):
            [item] = ReceivedItem.objects.prefetch_related('item__relateditem_set')
        with self.assertNumQueries(0):
            self.assertEqual(len(item.item.relateditem_set.all()), 3)


class TestMisc(TestCase):
    def test_str(self):
        self.assertEqual(str(ReceivedItem.item), 'tests.ReceivedItem.item')

    def test_check(self):
        self.assertEqual(ReceivedItem.item.check(), [])
        with patch.object(ReceivedItem.item, 'name', 'foo_'):
            self.assertEqual(len(ReceivedItem.item.check()), 1)
