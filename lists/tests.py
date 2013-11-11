from django.core.urlresolvers import resolve 
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page

from django.template.loader import render_to_string

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

	# Test that we get something back when we POST a new list item 
	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'

		response = home_page(request)

		self.assertIn('A new list item', response.content.decode())
		# Looks like the django render_to_string function can take a dict of passed form values
		expected_html = render_to_string(
			'home.html',
			{'new_item_text': 'A new list item'}
		)
		self.assertEqual(response.content.decode(), expected_html)