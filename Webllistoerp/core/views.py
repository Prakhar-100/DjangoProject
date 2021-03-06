from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import UpdateView, FormView
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic.base import View, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.utils.functional import cached_property
from core.models import CustomUser, UserHeirarchy
from django.contrib.auth.models import User
from core.forms import Login_form, UserForm
from chat.views import filter_channel_names
from django.views.generic import DetailView
from  chat.models import ChatGroupList
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
import json


def display_empname(request):
	# all_members = CustomUser.objects.select_related('username', 'first_name', 'last_name', 'designation')
	all_members = CustomUser.objects.only('id', 'username', 'first_name', 'last_name', 'designation')
	# all_members = CustomUser.objects.all()

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
	return {'all_members': all_members,'PM': PM, 'Web':Web,'CTO':CTO, 'DIR':DIR, 'TL': TL}

def filter_name(request):
	if request.user.designation == 'Director':
		# data = CustomUser.objects.all()
		# data = CustomUser.objects.iterator()
		data = CustomUser.objects.only('id', 'designation', 'username', 'first_name', 'last_name')
	else:
		obj1 = UserHeirarchy.objects.get(child__username = request.user.username)
		obj5 = CustomUser.objects.filter(username = obj1.usernm)
		mylist = [obj5[0].id, request.user.id]
		for ele in UserHeirarchy.objects.filter(usernm__username = request.user.username).select_related('usernm', 'child'):
			obj2 = CustomUser.objects.get(username = ele.child)
			mylist.append(obj2.id)
			for ele2 in UserHeirarchy.objects.filter(usernm__username = ele.child).select_related('usernm', 'child'):
				obj3 = CustomUser.objects.get(username = ele2.child)
				mylist.append(obj3.id)
				for ele3 in UserHeirarchy.objects.filter(usernm__username = ele2.child).select_related('usernm', 'child'):
					obj4 = CustomUser.objects.get(username = ele3.child)
					mylist.append(obj4.id)
		data = CustomUser.objects.filter(id__in = mylist).only('id', 'designation', 'username', 'first_name', 'last_name')
		# print(data.explain(verbose = True, analyze = True))
	return data

def form_data_filter(request):
	context1 = filter_name(request)
	Web = [ele for ele in context1 if ele.designation == 'Web Developer']
	DIR = [ele for ele in context1 if ele.designation == 'Director']
	TL  = [ele for ele in context1  if ele.designation == 'Tech Leader']
	PM  = [ele for ele in context1 if ele.designation == 'Project Manager']
	CTO = [ele for ele in context1 if ele.designation == 'Cheif Technical Officer']
	return {'Web': Web, 'DIR': DIR, 'TL':TL, 'PM': PM, 'CTO': CTO}


def filter_channel_names(request):
	chatlink = ChatGroupList.objects.only('member_name', 'admin_name', 'group_name', 'description')
	mylink, onelink, multilink = [], [], []

	for obj in chatlink:
		if request.user in obj.member_name.all():
			mylink.append(obj)

	for obj1 in mylink:
		if obj1.member_name.all().count() > 2:
			multilink.append(obj1)
		else:
			onelink.append(obj1)
	return onelink, multilink



class Index(DetailView):
	template_name = 'core/index.html'

	def get(self, request, *args, **kwargs):
		# onelink, multilink = filter_channel_names(request)
		context2 = form_data_filter(request)
		# mydict = {'onelink': onelink, 'multilink': multilink}
		return render(request, self.template_name, context2)



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

		f = self.form_class(request.POST)
		if f.is_valid():
			usermail = f.cleaned_data.get('user_email')
			password = f.cleaned_data.get('password')
			user = authenticate(email=usermail, password=password)
			if user is not None:
				login(request, user)
				return redirect('/index')
			else:
				error = "Please enter valid useremail and password"
				return render(request, self.template_name, {'form': f, 'key': error})
		return render(request, "registration/login.html")
	


class Promodel(View):
	""" This function is create a designation heirarchy of the users """
	template_name = 'core/profile.html'

	def get(self, request, *args, **kwargs):
		context =  display_empname(request)
		# onelink, multilink = filter_channel_names(request)
		# mydict = {'onelink': onelink, 'multilink': multilink}
		return render(request, self.template_name, context)


	def post(self, request, *args, **kwargs):
		user_id = int(request.POST.get('parent2'))
		for record in request.POST.getlist('child[]'):
			profilemodel = UserHeirarchy.objects.create(
														usernm_id = user_id,
														child_id = record
														)
		return HttpResponseRedirect('/index') 


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



class DesignationUpdate(FormView):
	template_name = 'core/designationupdate.html'

	def get(self, request, *args, **kwargs):
		# onelink, multilink = filter_channel_names(request)
		# mydict = {'onelink': onelink, 'multilink': multilink}
		context2 = form_data_filter(request)
		return render(request, self.template_name, context2)

	def post(self, request, *args, **kwargs):
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




