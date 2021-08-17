from django.contrib.messages.api import error
from django.db import models
import requests
import bcrypt
import re


class UserManager(models.Manager):
	def validator(self, post_data):
		"""validator for name, email, pw
		all key names come from form in index.html"""
		errors = {}
		# print(post_data.keys())
		# failing because its looking ofr 'first_name and so on
		# for login, this field doesn't exist, therefore need to split up validators
		if len(post_data['user_name']) < 3:
			errors["user_name"] = "Username should be at least 3 characters"
		if not post_data['user_name'].isalpha():
			errors["user_name"] = "Username should only be alphabetical characters"

		email_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
		if not email_re.match(post_data['email']):
			errors['email'] = "Invalid email address"

		# even if empty, filter won't break
		users_with_email = User.objects.filter(
			email=post_data['email'])
		if len(users_with_email) >= 1:
			errors['dupe'] = "Email is registered, choose another"

		if len(post_data['password']) < 12:
			errors['password'] = "Password is too short, 12 or more characters please"
		elif post_data['password'] != post_data['confirm_password']:
			errors['match'] = "Password does not match password confirmation"

		return errors

	
	def login_validator(self, post_data, request):
		"""validator for username nas pw
		request is for passing in session"""
		errors = {}
		if len(post_data['user_name']) < 3:
			errors["user_name"] = "Username should be at least 3 characters"
		if not post_data['user_name'].isalpha():
			errors["user_name"] = "Username should only be alphabetical characters"
			request.session['user_name'] = ""
		else:
			login_user = post_data['user_name'].lower()
			user = User.objects.filter(user_name=login_user)
			if user:
				logged_user = user[0]
				print(logged_user)
				if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
					request.session['userid'] = logged_user.id
				else:
					errors['pass'] = "Incorrect password, please try again."
			else:
				request.session['user_name'] = ""
				errors['user_name'] = "Username doesn't exist. Please register first."
		return errors




class User(models.Model):
	user_name = models.CharField(null=True, blank=True, default=None, max_length=20)
	# last_name = models.CharField(max_length=50)
	email = models.CharField(default='email',
							 max_length=20)
	# max_length to 255, since it could get cut off and therefore not comparing the same hash
	password = models.CharField(default='password',
								max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()


class Comment(models.Model):
	comment_text = models.TextField(default='comment_text')
	user = models.ForeignKey(User, related_name='comments', default=0, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()

