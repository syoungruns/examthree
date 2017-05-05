from __future__ import unicode_literals
from django.db import models
import re, datetime, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
	def reg(self, data):
		errors = [] #show user all errors at once
		#check that first and last name have at least two characters
		# and are both all letters (no numbers!)
		if len(data['f_name']) < 2:
			errors.append("First name must be at least two characters long.")
		if not data['f_name'].isalpha():
			errors.append("First name may only be letters.")
		# check that username is present and valid
		if data['u_name'] == '':
			errors.append("Username may not be blank.")
		# check that email is present and valid
		if data['e_mail'] == '':
			errors.append("Email may not be blank.")
		if not EMAIL_REGEX.match(data['e_mail']):
			errors.append("Please enter a valid email address.")
		#validate email uniqueness
		try:
			User.happiness.get(e_mail = data['e_mail'])
			print('dupe')
			errors.append("Email is already registered")
		except:
			pass

		# pw and confirm match
		if len(data['pw']) < 8:
			errors.append("Password must be at least eight characters long.")
		if data['pw'] != data['confirmpw']:
			errors.append("Password does not match Confirm Password.")

		# date of birth validation
		if data['dob'] == '':
			errors.append("Birthday is required.")
		elif datetime.datetime.strptime(data['dob'], '%Y-%m-%d') >= datetime.datetime.now():
			errors.append("Birthday may not be in the future!")

		if len(errors) == 0:
			# no errors
			print('no errors')
			data['pw'] = bcrypt.hashpw(data['pw'].encode('utf-8'), bcrypt.gensalt())
			new_user = User.happiness.create(f_name = data['f_name'], u_name = data['u_name'], e_mail = data['e_mail'], pw = data['pw'], dob = data['dob'])
			return {
				'new': new_user,
				'error_list': None
				}
		else:
			#yes errors
			print(errors)
			return {
				'new': None,
				'error_list': errors
			}

	def log(self, log_data):
		errors = []
		#check if user's account exists
		# try:
		found_user = User.happiness.get(e_mail = log_data['email'])
		print found_user.pw
		if bcrypt.hashpw(log_data['password'].encode('utf-8'), found_user.pw.encode('utf-8')) != found_user.pw.encode('utf-8'):
			errors.append("Incorrect password.")
		# except:
		# 	#email does not exist in the database
		# 	errors.append("Email not registered.")
		if len(errors) == 0:
			return {
				'logged_user': found_user,
				'list_errors': None
			}
		else:
			return {
				'logged_user': None,
				'list_errors': errors
			}

class User(models.Model):
	f_name = models.CharField(max_length = 45)
	u_name = models.CharField(max_length = 45)
	e_mail = models.CharField(max_length = 45)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	pw = models.CharField(max_length = 45)
	dob = models.DateField()
	happiness = UserManager()

class Quotes(models.Model):
	quotedby = models.CharField(max_length = 45)
	content = models.CharField(max_length = 45)
	user = models.ForeignKey(User, related_name = 'quotes_created')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

class AddToList(models.Model):
    user = models.ForeignKey(User, related_name = 'user_adds')
    quotes = models.ForeignKey(Quotes, related_name = 'quote_adds')
