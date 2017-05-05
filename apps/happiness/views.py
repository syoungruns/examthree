from django.shortcuts import render, redirect
from .models import User, Quotes, AddToList
from django.contrib import messages
from django.db.models import Count

# Create your views here.
def index(request):
	return render(request, 'happiness/index.html')

def register(request):
	data = {
		# name6   #somevalue
		'f_name': request.POST['f_name'],
		'u_name': request.POST['u_name'],
		'e_mail': request.POST['e_mail'],
		'pw': request.POST['pw'],
		'confirmpw': request.POST['confirmpw'],
		'dob': request.POST['dob']
	}

	reg_results = User.happiness.reg(data)

	if reg_results['new'] != None:
		request.session['user_id'] = reg_results['new'].id
		request.session['user_fname'] = reg_results['new'].f_name
		return redirect('/success')
	else:
		for error_str in reg_results['error_list']:
			messages.add_message(request, messages.ERROR, error_str)
		return redirect('/')

def success(request):
	current_user = User.happiness.get(id = request.session['user_id'])
	all_quotes = Quotes.objects.all().order_by('-created_at')[:3]
	myFavs = Quotes.objects.filter(quote_adds__user = current_user)
	myself = User.happiness.get(id = request.session['user_id'])
	myQuotes = Quotes.objects.exclude(quote_adds__user = current_user)

	context = {
	'quotes': all_quotes,
	'myQuotes': myQuotes,
	'myFavs': myFavs
	}

	return render(request, 'happiness/success.html', context)

def login(request):
	print request.POST
	p_data = {
		'email': request.POST['email'],
		'password': request.POST['password']
	}

	log_results = User.happiness.log(p_data)

	if log_results['list_errors'] != None:
		for error in log_results['list_errors']:
			messages.add_message(request, messages.ERROR, error)
		return redirect('/')
	else:
		request.session['user_id'] = log_results['logged_user'].id
		request.session['user_fname'] = log_results['logged_user'].f_name
		return redirect('/success')

def logout(request):
	request.session.clear()
	return redirect('/')

def add_quote(request):
	current_user = User.happiness.get(id = request.session['user_id'])
	danish = request.POST['quotedby']
	quiche = request.POST['message']
	Quotes.objects.create(quotedby = danish, content = quiche, user = current_user)
	return redirect('/success')

def destroy_quote(request, quote_id):
	# if request.method == 'POST':
	# 	print quote_id
	# 	a_quote = Quotes.objects.get(id = quote_id)
	# 	if a_quote.user.id == request.session['user_id']:
	# 		a_quote.delete()
	# 	else:
	# 		messages.add_message(request, messages.ERROR, "You're not allowed to do that!")
	favQuotez = Quotes.objects.get(id = quote_id)
	myself = User.happiness.get(id = request.session['user_id'])
	AddToList.objects.filter(user = myself, quotes = favQuotez).delete()
	return redirect('/success')

def users(request, user_id):
	myQuotes = Quotes.objects.filter(user = user_id)
	context = {
	'myQuotes': myQuotes
	}
	return render(request, 'happiness/users.html', context)

def favs(request, quote_id):
	favQuotez = Quotes.objects.get(id = quote_id)
	myself = User.happiness.get(id = request.session['user_id'])
	AddToList.objects.create(user = myself, quotes = favQuotez)
	return redirect('/success')
