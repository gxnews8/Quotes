from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Quote
import datetime
import bcrypt
import re

# Create your views here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]+$')
NAME = re.compile(r'[0,1,2,3,4,5,6,7,8,9]')


def index(request):
	return render (request, "index.html")

def register(request):
	if request.method == 'POST':
		user_tuple2 = User.userManager.register(request.POST['first_name'], request.POST['username'], request.POST['pw'], request.POST['c_pw'], request.POST['datehired'])
		if user_tuple2[0]:
			request.session['id'] = user_tuple2[1].id
			request.session['name'] = user_tuple2[1].first_name
			return redirect('/quotes')
		else:
			for i in user_tuple2[1]:
				messages.info( request, user_tuple2[1][i], extra_tags = 'rg')
		 	return redirect('/')

			#make user register again

def quotes(request):
	currentuser = User.userManager.get(id = request.session['id'])
	items = Quote.QuoteManager.all()
	othersitems = Quote.QuoteManager.exclude( adduser = currentuser).exclude( joinuser = currentuser)
	hisitems = Quote.QuoteManager.filter(adduser = currentuser)
	hisotheritems = Quote.QuoteManager.filter(joinuser = currentuser)

	context = {
		"curentuser" : currentuser,
		"hisitems" : hisitems,
		"hisotheritems" : hisotheritems,
		"othersitems" : othersitems,
		"items": items
	}
	return render (request, "quotes.html", context)

def login(request):

	if request.method == 'POST':
		user_tuple = User.userManager.login(request.POST['elogin'] , request.POST['Lpw'])
		if user_tuple[0]:
			request.session['id'] = user_tuple[1].id
			request.session['name'] = user_tuple[1].first_name
			#change request.session to message later or add request.session to flash message later
			return redirect('/quotes')
		else:
			for i in user_tuple[1]:
				messages.info( request, user_tuple[1][i], extra_tags = 'lg')
			return redirect('/')

def additem(request):
	if request.method == "GET":
		return render( request, 'additem.html')
	else:
		return redirect('/quotes')

def addingitem(request):
	if request.method =="POST":
		print "adding new item here"
		currentuser = User.userManager.get(id = request.session['id'])
		new_item = Quote.QuoteManager.createitem(currentuser, request.POST['itemname'], request.POST['quoted_by'])
		print "checking if adding process return true or false"
		if new_item[0]:
			print "Successfully adding new item"
			return redirect('/quotes')
		else:
			print "Cannot add new item to the wish list see the errors"

			for i in new_item[1]:
				messages.info( request, new_item[1][i])
		 	return redirect('/additem')

def joinninglist(request, id):
	if request.method == "GET":
		currentuser = User.userManager.get(id = request.session['id'])
		join = Quote.QuoteManager.joinlist(currentuser, id)
		if join[0]:
			print 'successfully join the list'
			return redirect('/quotes')
		else:
			print 'oh no something went wrong'
			return redirect('/quotes')

def users(request,id):
	if request.method == "GET":
		poster = User.objects.get(id = id)
		postcount = User.objects.filter(whoadd__adduser = id).count()
		postitems = Quote.QuoteManager.filter(adduser = id)

		context = {
			'count': postcount,
			'poster': poster,
			"items" : postitems,
		}

		return render( request,'users.html', context)
	else:
		return redirect('/quotes')

def removeitem(request,id):
	if request.method	== "GET":
		currentuser = User.userManager.get(id = request.session['id'])
		remove_item = Quote.QuoteManager.removeitem(currentuser, id)
		return redirect('/quotes')

def deleteitem(request,id):
	if request.method == "GET":
		currentuser = User.userManager.get(id = request.session['id'])
		delete_item = Quote.QuoteManager.deleteitem(currentuser, id)
		if delete_item[0]:
			return redirect('/quotes')
		else:
			print delete_item[1]
			return redirect('/quotes')


def logoff(request):
	request.session.clear()
	return	redirect('/')
