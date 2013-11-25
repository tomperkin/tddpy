from django.http import HttpRequest
from django.template.loader import render_to_string
from django.core.urlresolvers import resolve 
from django.test import TestCase
from lists.views import home_page
from lists.models import Item, List
from unittest import skip
from django.utils.html import escape

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


	def test_validation_errors_sent_back_to_home_page_template(self):
		response = self.client.post(
			'/lists/new',
			data={'item_text': ''}
		)
		
		self.assertEqual(Item.objects.all().count(), 0)
		self.assertTemplateUsed('home.html')
		expected_error = escape("You can't have an empty list item")
		self.assertContains(response, expected_error)





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

	def test_can_save_a_POST_request_to_an_existing_list(self): 
		other_list = List.objects.create()
		correct_list = List.objects.create()
		self.client.post(
			'/lists/%d/' % (correct_list.id,),
			data={'item_text': 'A new item for an existing list'}
		)

		# Does this not rely on test execution order??
		self.assertEqual(Item.objects.all().count(), 1)

		new_item = Item.objects.all()[0]
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)

	def test_POST_redirects_to_list_view(self):
		other_list = List.objects.create() 
		correct_list = List.objects.create()
		response = self.client.post(
			'/lists/%d/' % (correct_list.id,),
			data={'item_text': 'A new item for an existing list'}
		)
		
		self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

	def test_validation_errors_end_up_on_lists_page(self):
		myList = List.objects.create()

		response = self.client.post(
			'/lists/%d/' % (myList.id,),
			data={'item_text': ''}
		)
		
		self.assertEqual(Item.objects.all().count(), 0)
		self.assertTemplateUsed('list.html')
		expected_error = escape("You can't have an empty list item")
		self.assertContains(response, expected_error)

