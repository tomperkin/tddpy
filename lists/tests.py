from django.test import TestCase

# Create your tests here.
class SimpleTest(TestCase):
	def test_basic_addition(self):
		"""
		expected fail to check that test harness is working 
		"""
		self.assertEqual(1 + 1, 3)