from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.conf import settings
from .models import *
import bcrypt


def index(request):
	return render(request, 'index.html')


def register(request):
	"""registering and grabbing user id registration flow
	based off the model"""
	errors = User.objects.validator(request.POST)
	if len(errors) > 0:
		print("after first second")
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	else:
		# Create User
		hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
		user = User.objects.create(
			# first_name=request.POST['first_name'],
			# last_name=request.POST['last_name'],
			user_name=request.POST['user_name'],
			email=request.POST['email'], password=hash_pw
			# password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt().decode())
		)
		request.session['user_id'] = user.id
		# request.session['first_name'] = user.first_name
		return redirect('/search')


def login_user(request):
	"""email and pw, avoid bcrypt salt error
	check for user_name, then compare pw form field with db stored pw
	if user_name matches existing username, login
	otherwise, redirect to register"""

	if request.method == 'GET':
		return render(request, "login.html")
	
	errors = User.objects.login_validator(request.POST, request)


	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/login_user')

	user = User.objects.filter(
		user_name=request.POST['user_name'])  # why are we using filter here instead of get

	if len(user) > 0:		# if this isn't triggered, inner else statement executes
		logged_user = user[0]
		# use bcrypt's check_pw method, passing the hash from db and the pw from the form
		if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
			# if we get True after checking the password, we have to put the user id in session
			request.session['user_id'] = logged_user.id
			return redirect('/dash')
		else:
			messages.error(request, 'Username or password did not match')
	# if the passwords don't match, redirect back to a safe route
	return redirect("/login_user")


def dash(request):
	context = {
		"logged_user": User.objects.get(id=request.session['user_id'])
	}
	return render(request, 'search.html', context)


def search(request):
	"""users can search here"""
	context = {
		# 'first_name': request.session['first_name'],
		# 'messages': Comment.objects.all(),
		'comments': Comment.objects.all(),
	}
	# request.session['user_name'] = context.user_name
	return render(request, 'search.html', context)


def comment(request):
	"""post comments"""
	if request.method == 'POST':
		new_comment = Comment.objects.create(
			comment_text=request.POST['comment'],
			user=User.objects.get(id=request.session['user_id']),  # changed this from user to user_id
			# message=Message.objects.get(id=message_id)
		)
		new_comment.save()

	return redirect('/search')


def destroy(request):
	"""destroy session with clear method"""
	request.session.clear()
	return redirect('/')


def logout(request):
	"""logout session, back to home"""
	request.session.flush()
	print(request.session)
	return redirect('/')
