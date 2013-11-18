from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):	
	def test_layout_and_styling(self):
		# Edith goes to the homepage
		self.browser.get(self.server_url)
		self.browser.set_window_size(1024,768)

		# She notices that the input box is nicely centered
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] /2,
			512,
			delta=3
		)

		# She starts a new list and that's nicely centred as well
		inputbox.send_keys('testing\n')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] /2,
			512,
			delta=3
		)

