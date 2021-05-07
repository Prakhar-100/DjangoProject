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

# class Index(View):
	
# 	template_name = 'core/index.html'
	
# 	def get(self, request):
		
# 		all_members = CustomUser.objects.all()
# 		mylist = []
# 		i, n = 1, 0
# 		for ele in UserHeirarchy.objects.filter(usernm__username = request.user):
# 			obj2 = CustomUser.objects.get(username = ele.child)
# 			mylist.append(obj2) 
# 			for ele2 in UserHeirarchy.objects.filter(usernm__username = ele.child):
# 					obj3 = CustomUser.objects.get(username = ele2.child)
# 					mylist.append(obj3)
# 					mylist[n].id = i 
# 					i = i + 1
# 					n = n + 1
# 					for ele3 in UserHeirarchy.objects.filter(usernm__username = ele2.child):
# 						obj4 = CustomUser.objects.get(username = ele3.child)
# 						mylist.append(obj4)
# 						mylist[n].id = i 
# 						i = i + 1
# 						n = n + 1
# 			mylist[n].id = i 
# 			i = i + 1
# 			n = n + 1
# 		# userheirarchy = UserHeirarchy.objects.all()
# 		context = { 'obj': mylist , 'all_members': all_members}

# 		return render(request, self.template_name, context)

DATATABLES_SERVERSIDE_MAX_COLUMNS = 30

class DatatablesServerSideView(View):
    columns = []
    searchable_columns = []
    foreign_fields = {}
    model = None

    def __init__(self, *args, **kwargs):
        super(DatatablesServerSideView, self).__init__(*args, **kwargs)
        fields = {f.name: f for f in self.model._meta.get_fields()}

        model_columns = {}
        for col_name in self.columns:
            if col_name in self.foreign_fields:
                new_column = ForeignColumn(
                    col_name, self.model,
                    self.foreign_fields[col_name])
            else:
                new_column = Column(fields[col_name])

            model_columns[col_name] = new_column

        self._model_columns = model_columns
        self.foreign_fields = self.foreign_fields

    def get(self, request, *args, **kwargs):
    	if not request.is_ajax():
    		return HttpResponseBadRequest()
    	try:
    		params = self.read_parameters(request.GET)
    	except ValueError:
    		return HttpResponseBadRequest()

        # Prepare the queryset and apply the search and order filters
    	qs = self.get_initial_queryset()

    	if 'search_value' in params:
    		qs = self.filter_queryset(params['search_value'], qs)

    	if len(params['orders']):
        	qs = qs.order_by(
                *[order.get_order_mode() for order in params['orders']])

    	paginator = Paginator(qs, params['length'])

    	return HttpResponse(
            json.dumps(
                self.get_response_dict(paginator, params['draw'],
                                       params['start']),
                cls=DjangoJSONEncoder
            ),
            content_type="application/json")

    def read_parameters(self, query_dict):
        """ Converts and cleans up the GET parameters. """
        params = {field: int(query_dict[field]) for field
                  in ['draw', 'start', 'length']}

        column_index = 0
        has_finished = False
        column_links = []

        while column_index < DATATABLES_SERVERSIDE_MAX_COLUMNS and\
                not has_finished:
            column_base = 'columns[%d]' % column_index

            try:
                column_name = query_dict[column_base + '[name]']
                if column_name != '':
                    column_links.append(ColumnLink(
                        column_name,
                        self._model_columns[column_name],
                        query_dict.get(column_base + '[orderable]'),
                        query_dict.get(column_base + '[searchable]')))
                else:
                    column_links.append(PlaceholderColumnLink())
            except KeyError:
                has_finished = True

            column_index += 1

        orders = []
        order_index = 0
        has_finished = False
        while order_index < len(self.columns) and not has_finished:
            try:
                order_base = 'order[%d]' % order_index
                order_column = query_dict[order_base + '[column]']
                orders.append(Order(
                    order_column,
                    query_dict[order_base + '[dir]'],
                    column_links))
            except ColumnOrderError:
                pass
            except KeyError:
                has_finished = True

            order_index += 1

        search_value = query_dict.get('search[value]')
        if search_value:
            params['search_value'] = search_value

        params.update({'column_links': column_links, 'orders': orders})
        return params

    def get_initial_queryset(self):
    	if self.request.user.designation == 'Director':
    		newlist = self.model.objects.all()
    	else:
    		mylist = []
    		for ele in UserHeirarchy.objects.filter(usernm__username = self.request.user.username):
    			obj2 = self.model.objects.get(username = ele.child)
    			mylist.append(obj2.id)
    			for ele2 in UserHeirarchy.objects.filter(usernm__username = ele.child):
    				obj3 = self.model.objects.get(username = ele2.child)
    				mylist.append(obj3.id)

    				for ele3 in UserHeirarchy.objects.filter(usernm__username = ele2.child):
    					obj4 = self.model.objects.get(username = ele3.child)
    					mylist.append(obj4.id)
    		newlist = self.model.objects.filter(id__in = mylist)
    	return newlist

    def render_column(self, row, column):
        return self._model_columns[column].render_column(row)

    def prepare_results(self, qs):
        json_data = []

        for cur_object in qs:
            retdict = {fieldname: self.render_column(cur_object, fieldname)
                       for fieldname in self.columns}
            self.customize_row(retdict, cur_object)
            json_data.append(retdict)
        return json_data

    def get_response_dict(self, paginator, draw_idx, start_pos):
        page_id = (start_pos // paginator.per_page) + 1
        if page_id > paginator.num_pages:
            page_id = paginator.num_pages
        elif page_id < 1:
            page_id = 1

        objects = self.prepare_results(paginator.page(page_id))
        return {"draw": draw_idx,
                "recordsTotal": paginator.count,
                "recordsFiltered": paginator.count,
                "data": objects}

    def customize_row(self, row, obj):
        pass

    def choice_field_search(self, column, search_value):
        values_dict = self.choice_fields_completion[column]
        matching_choices = [val for key, val in six.iteritems(values_dict)
                            if key.startswith(search_value)]
        return Q(**{column + '__in': matching_choices})

    def filter_queryset(self, search_value, qs):
        search_filters = Q()
        for col in self.searchable_columns:
            model_column = self._model_columns[col]

            if model_column.has_choices_available:
                search_filters |=\
                    Q(**{col + '__in': model_column.search_in_choices(
                        search_value)})
            else:
                query_param_name = model_column.get_field_search_path()

                search_filters |=\
                    Q(**{query_param_name+'__istartswith': search_value})

        return qs.filter(search_filters)


class Index(TemplateView):
	template_name = 'core/index.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# context['all_members'] = CustomUser.objects.all()
		
		return context


class DataView_Json(DatatablesServerSideView):
	# Columns used in the DataTables
	template_name = "core/index.html"
	model = CustomUser
	columns = ['first_name', 'last_name', 'email', 'designation', 'username']
	# Columns in which searching is allowed
	searchable_columns = ['first_name', 'last_name', 'designation', 'username']

    

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

# class Record_Update(UpdateView):
# 	template_name = 'core/record_edit.html'
#     model = CustomUser
#     fields = ['first_name', 'last_name', 'email']
#     success_url = '/core/datatable'
#     form_class = UpdateForm

#     def get(self, request):
#         return render(request,self.template_name, {'form': form})



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
		send_mail( subject, message, email_from, recipient_list )

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



