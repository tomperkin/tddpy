from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError

class ListAndItemModelTest(TestCase):
	def test_saving_and_retrieving_items(self):
		# create and save a new List instance
		list_ = List()
		list_.save()

		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.list = list_
		first_item.save()
		
		second_item = Item()
		second_item.text = 'Item the second'
		second_item.list = list_
		second_item.save()
		
		saved_lists = List.objects.all()
		self.assertEqual(saved_lists.count(),1)
		self.assertEqual(saved_lists[0], list_)
	
		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)
		
		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(first_saved_item.list, list_)
		self.assertEqual(second_saved_item.text, 'Item the second')
		self.assertEqual(second_saved_item.list, list_)


	def test_cannot_save_empty_list_items(self):
		list1 = List.objects.create()
		item = Item(list=list1, text='')
		with self.assertRaises(ValidationError):
			item.save()

	def test_absolute_url(self):
		list_ = List.objects.create()
		self.assertEqual(list_.get_absolute_url(), '/lists/%d/' % (list_.id,) )

	def test_cannot_save_duplicate_items(self):
		list_ = List.objects.create()
		Item.objects.create(list=list_, text='blah')
		with self.assertRaises(ValidationError):
			Item.objects.create(list=list_, text='blah')

	def test_CAN_save_same_item_to_different_lists(self):
		list1 = List.objects.create()
		list2 = List.objects.create()
		Item.objects.create(list=list1, text='blah') 
		Item.objects.create(list=list2, text='blah') # should not raise

	def test_list_ordering(self):
		list1 = List.objects.create()
		item1 = Item.objects.create(list=list1, text='item 1') 
		item2 = Item.objects.create(list=list1, text='item 2') 
		item3 = Item.objects.create(list=list1, text='item 3') 

		self.assertEqual(
			list(Item.objects.all()),
			[item1, item2, item3]
		)

	# Test that an Item's str representation is its text
	def test_string_representation(self):
		list1 = List.objects.create()
		item1 = Item.objects.create(list=list1, text='blah blah')

		self.assertEqual(str(item1), item1.text)
