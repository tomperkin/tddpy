from django.shortcuts import render
from django.shortcuts import redirect
from lists.models import Item, List
from lists.forms import ItemForm
from django.core.exceptions import ValidationError

def home_page(request):
	return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	error = None
	if request.method == 'POST':
		try:
			Item.objects.create(text = request.POST['item_text'], list=list_)
			return redirect(list_) # uses get_absolute_url under the covers
		except ValidationError:
			error = "You can't have an empty list item"


	return render(request, 'list.html', {'list': list_, "error": error})


def new_list(request):
	list_ = List.objects.create()
	try:
		Item.objects.create(text=request.POST['item_text'], list=list_)
	except ValidationError:
		error_text = "You can't have an empty list item"
		return render(request, 'home.html', {"error": error_text})
	return redirect(list_)
