from django.shortcuts import render
from django.shortcuts import redirect
from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm

def home_page(request):
	return render(request, 'home.html', {'form': ItemForm()})

def new_list(request):
	form = ItemForm(data=request.POST)

	if form.is_valid():
		list_ = List.objects.create()
		form.save(for_list=list_)
		return redirect(list_)
	else:
		return render(request, 'home.html', {"form": form})

def view_list(request, list_id):

	list_ = List.objects.get(id=list_id)
	form = ExistingListItemForm(for_list = list_, data = request.POST or None)

	if form.is_valid():
		form.save()
		return redirect(list_) # uses get_absolute_url under the covers to work out the URL to redirect to
	
	# Failed validation, or a GET
	return render(request, 'list.html', {'list': list_, 'form': form})


	
