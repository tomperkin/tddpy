from django.core.urlresolvers import resolve 
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page

from django.template.loader import render_to_string
from lists.models import Item

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

	# Test that GETting the home_page view doesn't create a list item
	def test_home_page_only_saves_items_when_necessary(self):
		request = HttpRequest()
		home_page(request)
		self.assertEqual(Item.objects.all().count(), 0)

	# Test that we get something back when we POST a new list item 
	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'

		response = home_page(request)

		# Test that the ORM actually persists out new 'Item' object
		self.assertEqual(Item.objects.all().count(), 1)
		new_item = Item.objects.all()[0]
		self.assertEqual(new_item.text, 'A new list item')

	# Test that we get a 302 redirect to '/' in return
	def test_home_page_redirects_after_POST(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'

		response = home_page(request)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/')

	# Test that our page can displat multiple list items
	def test_home_page_displays_all_list_items(self):
		# pump them directly into the database - no need to go through the view
		Item.objects.create(text='item 1')
		Item.objects.create(text='item 2')

		request = HttpRequest()
		response = home_page(request)

		self.assertIn('item 1', response.content.decode())
		self.assertIn('item 2', response.content.decode())


class ItemModelTest(TestCase):
	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.save()
		
		second_item = Item()
		second_item.text = 'Item the second'
		second_item.save()
		
		saved_items = Item.objects.all()
		
		self.assertEqual(saved_items.count(), 2)
		
		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(second_saved_item.text, 'Item the second')

