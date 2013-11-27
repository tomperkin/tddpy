from django.db import models
from django.shortcuts import resolve_url

# Create your models here.
class List(models.Model):
	def get_absolute_url(self):
		return resolve_url('view_list', self.id)

class Item(models.Model):
	text = models.TextField()
	list = models.ForeignKey(List)

	class Meta:
		ordering = ('id',)
		unique_together = ('list', 'text')

	# Override the save method to force a validation check in model layer
	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)

	def __str__(self):
		return self.text