from django.http import HttpRequest
from django.template.loader import render_to_string
from django.core.urlresolvers import resolve 
from django.test import TestCase
from lists.views import home_page
from lists.models import Item, List
from unittest import skip

class HomePageTest(TestCase):
	def test_root_url_resolves_to_home_page_view(self): 
		found = resolve('/') 
		self.assertEqual(found.func, home_page)
	
	# Test that we get the expected template back from a request to /
	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		
		self.assertEqual(response.content.decode(), expected_html)

class NewListTest(TestCase):
	# Test that the ORM actually persists out new 'Item' object
	def test_saving_a_POST_request(self):
		
		self.client.post(
			 '/lists/new',
			 data={'item_text': 'A new list item'}
		)
				
		self.assertEqual(Item.objects.all().count(), 1)
		new_item = Item.objects.all()[0]
		self.assertEqual(new_item.text, 'A new list item')

	# Test that we get a 302 redirect to our newly minted list in response to the POST
	def test_redirects_after_POST(self):
		
		response = self.client.post(
			 '/lists/new',
			 data={'item_text': 'A new list item'}
		)

		new_list = List.objects.all()[0]
		self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

class NewItemTest(TestCase):
	def test_can_save_a_POST_request_to_an_existing_list(self): 
		other_list = List.objects.create()
		correct_list = List.objects.create()
		self.client.post(
			'/lists/%d/new_item' % (correct_list.id,),
			data={'item_text': 'A new item for an existing list'}
		)

		# Does this not rely on test execution order??
		self.assertEqual(Item.objects.all().count(), 1)

		new_item = Item.objects.all()[0]
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)

	def test_redirects_to_list_view(self):
		other_list = List.objects.create() 
		correct_list = List.objects.create()
		response = self.client.post(
			'/lists/%d/new_item' % (correct_list.id,),
			data={'item_text': 'A new item for an existing list'}
		)
		
		self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

	@skip
	def test_cannot_add_empty_list_items(self):
		# Edith goes to the home page and accidentally tries to submit
		# an empty list item. She hits Enter on the empty input box

		# The home page refreshes, and there is an error message saying
		# that list items cannot be blank

		# She tries again with some text for the item, which now works

		# Perversely, she now decides to submit a second blank list item

		# She receives a similar warning on the list page

		# And she can correct it by filling some text in
		self.fail('write me!')



class ListViewTest(TestCase):
	
	# Test that the list view uses its own template in the unique list URL
	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/' % (list_.id,))
		self.assertTemplateUsed(response, 'list.html')

	# Test that we only get items from the correct list
	def test_displays_only_items_for_that_list(self):
		# pump them directly into the database - no need to go through the view
		correct_list = List.objects.create()
		Item.objects.create(text='item 1', list=correct_list)
		Item.objects.create(text='item 2', list=correct_list)

		other_list = List.objects.create()
		Item.objects.create(text='other item 1', list=other_list)
		Item.objects.create(text='other item 2', list=other_list)

		response = self.client.get('/lists/%d/' % (correct_list.id,))

		self.assertContains(response, 'item 1')
		self.assertContains(response, 'item 2')
		self.assertNotContains(response, 'other item 1')
		self.assertNotContains(response, 'other item 2')

	def test_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.get('/lists/%d/' % (correct_list.id,))
		self.assertEqual(response.context['list'], correct_list)


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


