from __future__ import absolute_import, unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import AttendanceInfo, DayoffForm
from core.models import CustomUser, UserHeirarchy
from .somewhere import handle_uploaded_file
from .models import AttendanceModel, AttendanceData, DatewiseData, HolidayData, UserDayoffData
from .serializers import AttendanceSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AttendanceSerializer, AttendanceDataSerializer
from rest_framework import status
from attendance.get_face_encoding import calculate_face_encoding
from rest_framework.views import APIView
from django.http import Http404
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views import View
from django.views.generic import View
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.generic import View
from attendance.parameter import (
    Column, ForeignColumn,
    ColumnLink, PlaceholderColumnLink,
    Order, ColumnOrderError)
import json
import datetime
import time
import calendar
from notifications.signals import notify


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
                cls = DjangoJSONEncoder
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
            mylist = self.model.objects.all()
        else:
            ele = self.request.user.email
            mylist = self.model.objects.filter(name = ele[:ele.rfind('@')])
        return mylist

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



class Home(TemplateView):
	template_name = "attendance/home.html"
    

class AttendanceDataViewJson(DatatablesServerSideView):
    # Columns used in the DataTables
    template_name = "attendance/home.html"
    model = DatewiseData
    columns = ['id', 'name', 'date', 'week', 'time_in','time_out', 'work_status']
    searchable_columns = ['name']

def display_empname():
    all_members = CustomUser.objects.all()
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

def attendance_data(request):
    if request.method == 'POST':
        emp_id, emp_image= request.POST['name2'], request.FILES['userimage']
        custom_user = CustomUser.objects.get(id = emp_id)
		# Image is encoded using calculate_face_encoding method
        en_image = str(emp_image)
        image_path = f'/home/dell/images/{en_image}'
        encod_image = calculate_face_encoding(image_path)
        AttendanceModel.objects.create(emp = custom_user,image = emp_image,encod_image  = encod_image)
        return redirect('/attendance/home')
    context = display_empname()
    return render(request, 'attendance/att_form.html', context)


class DataCollection(APIView):

	def get(self, request, format=None):
		snippets = AttendanceModel.objects.all()
		serializer = AttendanceSerializer(snippets, many=True)
		return Response(serializer.data)

def formatted_time(ele):
    num = ele.rfind('(')
    ele2, ele3 = ele[:num - 1], ele[num+1:len(ele)-1]
    date_obj = datetime.datetime.strptime(ele2, '%d-%b-%Y').date()
    time_obj = datetime.datetime.strptime(ele3, '%H:%M:%S.%f').time()
    time_obj2 = time_obj.strftime("%I:%M %p")
    return time_obj, time_obj2, date_obj

def user_attendance_update(obj3, time_obj, time_obj2):
    t2 = datetime.datetime.strptime(obj3[0].time_in, '%I:%M %p')
    t3 = datetime.timedelta(hours = time_obj.hour,minutes = time_obj.minute) - datetime.timedelta(hours = t2.hour, minutes = t2.minute)
    if t3 >= datetime.timedelta(hours = 4) and t3 <= datetime.timedelta(hours = 5):
        obj3.update(time_out = time_obj2, work_status = "Half Day Working")
    elif t3 >= datetime.timedelta(hours = 7) and t3 <= datetime.timedelta(hours = 10):
        obj3.update(time_out = time_obj2, work_status = "Full Day Working")
    else:
        pass


def weekday_attendance_record(date_obj, nm):
    for i in range(1,3):
        DatewiseData.objects.create(
                    name = nm,
                    date = datetime.date(date_obj.year, date_obj.month, date_obj.day + i),
                    week = calendar.day_name[datetime.date(date_obj.year, date_obj.month, date_obj.day + i).weekday()],
                    time_in  = "-----",
                    time_out = "-----", 
                    work_status = 'Weekend'
                )

def weekend_attendance_update(obj3, time_obj2):
    obj3.update(time_in = time_obj2)

def holiday_attendance_record(nm, date_obj):
    month_list = []
    
    for ele in HolidayData.objects.all():
        month_list.append({'day': ele.date.day, 'month': ele.date.month, 'year': ele.date.year })

    for ele1 in month_list:
        if date_obj.month == ele1['month']:
            obj6 = HolidayData.objects.get(date = datetime.date(ele1['year'], ele1['month'], ele1['day']))
            DatewiseData.objects.create(
                name = nm,
                date = obj6.date,
                week = calendar.day_name[obj6.date.weekday()],
                time_in  = "-----",
                time_out = "-----",
                work_status = 'Holiday'
            )


class PostCollection(APIView):
    serializer_class = AttendanceDataSerializer
    def post(self, request, format=None):
        data = request.data
        serializer = self.serializer_class(data = data)
        if serializer.is_valid():
            serializer.save()
            ele = request.data['timestamp']
            time_obj, time_obj2, date_obj = formatted_time(ele)
            obj3 = DatewiseData.objects.filter(name = request.data['emp']).filter(date = date_obj)
            if obj3:
                # Update the record of Saturday and Sunday
                if calendar.day_name[date_obj.weekday()] == ('Saturday' or 'Sunday'):
                    if obj3[0].time_in != "-----":
                        user_attendance_update(obj3, time_obj, time_obj2)
                    else:
                        weekend_attendance_update(obj3, time_obj2)
                else:                    
                    user_attendance_update(obj3, time_obj, time_obj2)

            else:
                DatewiseData.objects.create(
                                    name = request.data['emp'],
                                    date = date_obj,
                                    week = calendar.day_name[date_obj.weekday()],
                                    time_in  = time_obj2,
                                    time_out = time_obj2,
                                    work_status = 'Working'
                                    )

                # If the particular week is Saturday or Sunday
                if calendar.day_name[date_obj.weekday()] == 'Friday':
                    weekday_attendance_record(date_obj, request.data['emp'])

                # If a particular month have 1st day
                if date_obj.day == 1:
                    holiday_attendance_record(request.data['emp'],date_obj)


            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

DATATABLES_SERVERSIDE_MAX_COLUMNS = 30

def get_dates(week, month, year=2021):
    return calendar.monthcalendar(year,month)[week]

def filter_attendance_name(request):
    if request.user.designation == 'Director':
        newlist = CustomUser.objects.all()
    else:
        mylist = [request.user.id]
        for ele in UserHeirarchy.objects.filter(usernm__username = request.user.username):
            obj2 = CustomUser.objects.get(username = ele.child)
            mylist.append(obj2.id)
            for ele2 in UserHeirarchy.objects.filter(usernm__username = ele.child):
                obj3 = CustomUser.objects.get(username = ele2.child)
                mylist.append(obj3.id)
                for ele3 in UserHeirarchy.objects.filter(usernm__username = ele2.child):
                    obj4 = CustomUser.objects.get(username = ele3.child)
                    mylist.append(obj4.id)
        newlist = CustomUser.objects.filter(id__in = mylist)
    return newlist

def attendance_form_filter(context, context1):
    Web = [ele for ele in context['Web'] if ele in context1]
    DIR = [ele for ele in context['DIR'] if ele in context1]
    TL  = [ele for ele in context['TL']  if ele in context1]
    PM  = [ele for ele in context['PM'] if ele in context1]
    CTO = [ele for ele in context['CTO'] if ele in context1]
    return {'Web': Web, 'DIR': DIR, 'TL':TL, 'PM': PM, 'CTO': CTO}



def attendance_form(request):
    context =  display_empname()
    context1 = filter_attendance_name(request)
    data = attendance_form_filter(context, context1) 
    return render(request, 'attendance/attendance_form.html', data)


def load_names(request):
    name, week, month = request.GET.get('name'), request.GET.get('week'), request.GET.get('month')
    tup, dict2, week_data  = [], {}, []
    obj1 = DatewiseData.objects.filter(name = name[:name.rfind('@')])

    # Filter data monthly as per individual user
    for ele in obj1:
        if ele.date.month == int(month):
            tup.append(ele.id)
    obj2 = DatewiseData.objects.filter(id__in = tup)

    # Calling function so that we can get dates as per week
    obj3 = get_dates(int(week), int(month))

    # Filtering data weekly as per individual user
    for ele1 in obj2:
        if ele1.date.day in obj3:
            week_data.append(ele1.id)
    obj4 = list(DatewiseData.objects.filter(id__in = week_data).values())
    return JsonResponse(obj4, safe=False)

def load_names_monthly(request):
    name, week, month = request.GET.get('name'), request.GET.get('week'), request.GET.get('month')
    tup = []
    obj1 = DatewiseData.objects.filter(name = name[:name.rfind('@')])

    # Filter data monthly as per individual user
    for ele in obj1:
        if ele.date.month == int(month):
            tup.append(ele.id)
    obj2 = DatewiseData.objects.filter(id__in = tup)
    obj5 = list(obj2.values())
    return JsonResponse(obj5, safe=False)

def dayoff_form(request):
    username = request.user.email
    name = username[:username.rfind('@')]
    if request.method == 'POST':
        calen1, calen2 =  request.POST['calen1'], request.POST['calen2']
        rec1, rec2 = request.POST['hr'], request.POST['tl']
        recp1 = CustomUser.objects.get(email = rec1)
        recp2 = CustomUser.objects.get(email = rec2)
        sender = CustomUser.objects.get(email = username)
        message = str(calen1) +'@'+ str(calen2)
        data = str(sender)+" wants to take leave from "+str(calen1)+" to "+str(calen2)+" because "+ request.POST['reason']
        UserDayoffData.objects.create(
                                  name = username,
                                  date = calen1,
                                  hr_approval = "Not Approved",
                                  tl_approval = "Not Approved",
                                  leave_reason = request.POST['reason']
                               )
        notify.send(sender = sender, 
                    recipient = recp2, 
                    verb = message, 
                    description = data,
                    action_object = recp1)
        return redirect('/attendance/dayoff/form')
    return render(request, 'attendance/dayoff_form.html', display_empname())

def notifications_page(request):
    data = request.user.notifications.unread()
    return render(request, 'attendance/notifications.html', {'data': data})

def tl_leave_approve(request, name, date, recp):
    data = request.user.notifications.unread()
    date1 = date[:date.rfind('@')]
    date2 = date[date.rfind('@') + 1:]
    object1 = UserDayoffData.objects.get(name = name, date = date1)
    object1.tl_approval = 'Approved'
    object1.save()
    object2 = CustomUser.objects.get(email = request.user.email)
    sender = CustomUser.objects.get(email = name)
    recp2 = CustomUser.objects.get(email = recp)
    data1 = str(sender)+" wants to take leave from "+str(date1)+" to "+str(date2)+" because "+ str(object1.leave_reason) +" and  approved by "+str(request.user.email)
    notify.send(sender = sender,
                recipient = recp2,
                verb = date,
                description = data1)
    return render(request, 'attendance/notifications.html', {'data': data})

def hr_leave_approve(request, name, date):
    data = request.user.notifications.unread()
    date1 = date[:date.rfind('@')]
    date2 = date[date.rfind('@') + 1:]

    object2 = CustomUser.objects.get(email = request.user.email)
    object1 = UserDayoffData.objects.get(name = name, date = date1)

    object1.hr_approval = 'Approved'
    object1.save()

    # Record of the user have been stored as Day Off
    date_obj1 = datetime.datetime.strptime(date1, '%Y-%m-%d').date()
    date_obj2 = datetime.datetime.strptime(date2, '%Y-%m-%d').date()
    date_diff = datetime.timedelta(days = date_obj2.day) - datetime.timedelta(days = date_obj1.day)
    num = 0
    if date_diff.days == 0:
        DatewiseData.objects.create(
                        name = name[:name.rfind('@')],
                        date = date_obj1,
                        week = calendar.day_name[date_obj1.weekday()],
                        time_in  = "-----",
                        time_out = "-----",
                        work_status = 'Leave'
                        )

    for i in range(0,date_diff.days + 1):
        mydate = date_obj1.day + num
        DatewiseData.objects.create(
                                name = name[:name.rfind('@')],
                                date = datetime.date(2021, date_obj1.month, mydate),
                                week = calendar.day_name[datetime.date(2021, 3, mydate).weekday()],
                                time_in  = "-----",
                                time_out = "-----",
                                work_status = 'Leave'
                            )
        num = num + 1
    return render(request, 'attendance/notifications.html', {'data': data})

def hr_not_approve(request, name, date):
    data = request.user.notifications.unread()
    return render(request, 'attendance/notifications.html', {'data': data})

def tl_leave_not_approve(request, name, date, recp):
    data = request.user.notifications.unread()
    date1 = date[:date.rfind('@')]
    date2 = date[date.rfind('@') + 1:]

    object2 = CustomUser.objects.get(email = request.user.email)
    object1 = UserDayoffData.objects.get(name = name, date = date1)

    # If the user is hr then the record is updated as Approved
    if object2.designation != "Cheif Technical Officer":       
        # If the user is not hr then the record is updated as Not Approved
        object1.tl_approval = 'Not Approved'
        object1.save()
        sender = CustomUser.objects.get(email = name)
        recp2 = CustomUser.objects.get(email = recp)
        data1 = str(sender)+" wants to take leave from "+str(date1)+" to "+str(date2)+" but not approved by "+str(request.user.email)
        notify.send(sender = sender, recipient = recp2, 
                      verb = "not approve",
                      description = data1)
    return render(request, 'attendance/notifications.html', {'data': data})

def remove_holiday(request, pk):
    obj1 = HolidayData.objects.get(id = pk)
    obj1.delete()
    return redirect('/attendance/holidays')


def holiday_display(request):
    data = HolidayData.objects.all()
    if request.method == "POST":
        HolidayData.objects.create(
                            date = request.POST['calen1'],
                            occasion = request.POST['occassion']
                            )
    return render(request, 'attendance/holiday.html',{'data': data})




