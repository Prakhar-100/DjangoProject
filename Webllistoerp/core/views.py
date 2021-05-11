from __future__ import absolute_import, unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import Login_form, UserForm, UpdateForm, ProfileForm, DesignationUpdateForm
from .models import CustomUser, UserHeirarchy
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views import View
from django.views.generic import View
from django.conf import settings
from django.core.mail import send_mail
from core.parameter import (
    Column, ForeignColumn,
    ColumnLink, PlaceholderColumnLink,
    Order, ColumnOrderError)
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
# from django.utils import six
import json
from itertools import chain


def filter_name(request):
    if request.user.designation == 'Director':
    	data = CustomUser.objects.all()
    else:
    	obj1 = UserHeirarchy.objects.filter(child__username = request.user.username)
    	obj5 = CustomUser.objects.filter(username = obj1[0].usernm)
    	mylist = [obj5[0].id, request.user.id]
    	for ele in UserHeirarchy.objects.filter(usernm__username = request.user.username):
    		obj2 = CustomUser.objects.get(username = ele.child)
    		mylist.append(obj2.id)
    		for ele2 in UserHeirarchy.objects.filter(usernm__username = ele.child):
    			obj3 = CustomUser.objects.get(username = ele2.child)
    			mylist.append(obj3.id)
    			for ele3 in UserHeirarchy.objects.filter(usernm__username = ele2.child):
    				obj4 = CustomUser.objects.get(username = ele3.child)
    				mylist.append(obj4.id)
    	data = CustomUser.objects.filter(id__in = mylist).order_by('designation')
    return data


def form_data_filter(context1):
    Web = [ele for ele in context1 if ele.designation == 'Web Developer']
    DIR = [ele for ele in context1 if ele.designation == 'Director']
    TL  = [ele for ele in context1  if ele.designation == 'Tech Leader']
    PM  = [ele for ele in context1 if ele.designation == 'Project Manager']
    CTO = [ele for ele in context1 if ele.designation == 'Cheif Technical Officer']
    return {'Web': Web, 'DIR': DIR, 'TL':TL, 'PM': PM, 'CTO': CTO}

def index(request):
	context1 = filter_name(request)
	context = form_data_filter(context1)
	return render(request, 'core/index.html', context)

class Sign_up(FormView):
	# Specify name of template
	template_name = 'core/sign_up.html'

	# Specify the form you want to use
	form_class = UserForm

	# url to redirect after successfully updating details
	success_url = '/index/'

	def form_valid(self, form):
		useremail = form.cleaned_data['email']
		user = form.save(commit=False)
		user.username = useremail
		user.save()
		form.save()
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
		return super().form_valid(form)


class Login1(View):
	form_class = Login_form
	template_name = 'registration/login.html'

	def get(self, request):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request):
		usermail = request.POST['user_email']
		password = request.POST['password']
		user = authenticate(email=usermail, password=password)

		if user is not None:
			login(request, user)
			return redirect('/index')
		else:
			return HttpResponse("Username and password is incorrect")
		return render(request, "registration/login.html")
	

@login_required
def record_delete(request, member_id):
	""" This function will delete the user record from the datatable """
	obj = CustomUser.objects.filter(id = str(member_id))
	obj.delete()
	all_members = CustomUser.objects.all()
	return render(request, 'core/datatable.html', {'all_members': all_members})


def record_update(request, member_id):	
	""" This function will update the firstname, lastname, and email of user """
	obj = CustomUser.objects.filter(id = str(member_id))
	form = UpdateForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			obj.update(first_name = form.cleaned_data['first_name'])
			obj.update(last_name = form.cleaned_data['last_name'])
			obj.update(email = form.cleaned_data['email'])
			# obj.save()
			# messages.success(request, _('Your profile was successfully updated!'))
			return redirect('/core/datatable')
		else:
			messages.error(request, _('Please correct the error below.'))
		
	return render(request, 'core/record_edit.html', {'form': form})


class Logout_View(View):
    def get(self, request):
        logout(request)
        return render(request, 'core/logout.html', {})


def promodel(request):
	""" This function is create a designation heirarchy of the users """
	context = {}
	all_members = CustomUser.objects.all()
	if request.method == 'POST':
		user_id = int(request.POST.get('usernm'))
		
		for record in request.POST.getlist('child[]'):
			profilemodel = UserHeirarchy.objects.create(
					usernm_id = user_id,
					child_id = record
					)
		
		return redirect('/index')
	PM,Web,CTO,TL,DIR = [],[],[],[],[]
	for member in all_members:
		if member.designation == 'Project Manager':
			PM.append(member)
		elif member.designation == 'Web Developer':
			Web.append(member)
		elif member.designation == 'Cheif Technical Officer':
			CTO.append(member)
		elif member.designation == 'Director':
			DIR.append(member)
		else:
			TL.append(member)


	context = {'all_members':all_members, 'PM': PM, 'Web':Web, 'CTO':CTO, 'DIR':DIR, 'TL': TL} 
	return render(request, 'core/profile.html', context)
	

def datatable(request):
	""" This function is used to show the records of all the users in the database """
	all_members = CustomUser.objects.all()
	return render(request, 'core/datatable.html', {'all_members': all_members})


def load_names(request):
	""" This function is used to pass the record of the user on ajax request 
	  """
	usernmId = request.GET.get('usernmId')
	choice = []
	dict2 = {}
	queryset = CustomUser.objects.all()
	obj = CustomUser.objects.get(id = usernmId)
	for i in queryset:
		if obj.designation == 'Project Manager' and i.designation == 'Tech Leader':
			choice.append({"id":i.id, "name":i.username, "designation": i.designation,
				"first_name": i.first_name, "last_name": i.last_name})
		elif obj.designation == 'Director' and i.designation == 'Cheif Technical Officer':
			choice.append({"id":i.id, "name":i.username, "designation": i.designation,
				"first_name": i.first_name, "last_name": i.last_name})
		elif obj.designation == 'Cheif Technical Officer' and i.designation == 'Project Manager':
			choice.append({"id":i.id, "name":i.username, "designation": i.designation,
				"first_name": i.first_name, "last_name": i.last_name})
		elif obj.designation == 'Tech Leader' and i.designation == 'Web Developer':
			choice.append({"id":i.id, "name":i.username, "designation": i.designation,
				"first_name": i.first_name, "last_name": i.last_name})
		elif obj.designation == 'Cheif Technical Officer' and i.designation != 'Director':
			choice.append({"id":i.id, "name":i.username, "designation": i.designation,
				"first_name": i.first_name, "last_name": i.last_name})
	return JsonResponse(choice, safe=False)


def designation_update(request):
	""" This function is used to update the designation of the user and 
	update the User Heirarchy """
	context = {}
	all_users = CustomUser.objects.all()
	# all_users2 = UserHeirarchy.objects.all()
	if request.method == 'POST':
		# Fetching child name
		child_name = request.POST.get('child2')
		# Fetching parent name
		parent_name = request.POST.get('parent2')
		obj1 = CustomUser.objects.get(username = str(parent_name))

		# Updating designation of CustomUser model
		obj2 = CustomUser.objects.get(username = str(child_name))
		obj2.designation = request.POST.get('designation2')
		obj2.save()

		# Updating the UserHeirarchy data	
		obj3 = UserHeirarchy.objects.filter(usernm_id = obj2.id)
		obj4 = UserHeirarchy.objects.get(child_id = obj2.id)

		for record in obj3:
			record.usernm_id = obj4.usernm_id
			record.save()

		# Updating Userheirarchy record
		obj4.usernm_id = obj1.id
		obj4.save()

		subject = 'Hi user'
		message = f'You have been promoted.'
		email_from = settings.EMAIL_HOST_USER
		recipient_list = ["somil.jainland@gmail.com", ]
		# send_mail( subject, message, email_from, recipient_list )

		return redirect('/index')

	PM,Web,CTO,TL,DIR = [],[],[],[],[]
	for member in all_users:
		if member.designation   == 'Project Manager':
			PM.append(member)
		elif member.designation == 'Web Developer':
			Web.append(member)
		elif member.designation == 'Cheif Technical Officer':
			CTO.append(member)
		elif member.designation == 'Director':
			DIR.append(member)
		else:
			TL.append(member)

	context = {'all_users': all_users, 'PM': PM, 'Web': Web, 'CTO': CTO, 'DIR':DIR, 'TL':TL}
	return render(request, 'core/designationupdate.html', context)


# def attendance(request):
# 	return render(request, 'core/attendance.html', {})



