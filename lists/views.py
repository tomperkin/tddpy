from django.shortcuts import render
from django.shortcuts import redirect
from lists.models import Item

def home_page(request):

	# If it's a POST, then create the new Item
	if request.method == 'POST':
		Item.objects.create(text=request.POST['item_text'])
		return redirect('/')

	items = Item.objects.all()
	# can add an optional dictionary of values to the render call, making the stuff 
	#  available to the template's context 
	return render(request, 'home.html', {'items': items})