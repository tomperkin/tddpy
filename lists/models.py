from django.db import models

# Create your models here.
class List(models.Model):
	pass

class Item(models.Model):
	text = models.TextField()
	list = models.ForeignKey(List)

	# Override the save method to force a validation check in model layer
	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)

