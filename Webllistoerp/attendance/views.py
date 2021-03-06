from attendance.models import AttendanceModel, AttendanceData, DatewiseData, HolidayData, UserDayoffData, TimeSheetData
from .serializers import AttendanceSerializer, AttendanceDataSerializer
from django.views.generic import TemplateView, View, DetailView, ListView
from django.views.generic.edit import FormView, UpdateView, CreateView
from django.http.response import HttpResponse, HttpResponseBadRequest
from attendance.get_face_encoding import calculate_face_encoding
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic.detail import DetailView
from core.models import CustomUser, UserHeirarchy
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import AttendanceSerializer
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from chat.views import filter_channel_names
from notifications.signals import notify
from rest_framework.views import APIView
from django.core.mail import send_mail
from chat.models import ChatGroupList
from django.conf import settings
from django.http import Http404
from rest_framework import status
from django.views import View
from dateutil import tz 
import calendar
import datetime
import time
import json




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


def display_empname():
    # all_members = CustomUser.objects.all()
    all_members = CustomUser.objects.only('id', 'username', 'first_name', 'last_name', 'designation')
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


class EmployeeData(FormView):

    def get(self, request, *args, **kwargs):
        context = display_empname()
        # onelink, multilink = filter_channel_names(request)
        # mydict = {'onelink': onelink, 'multilink': multilink}
        return render(request, 'attendance/att_form.html', context)

    def post(self, request, *args, **kwargs):
        emp_id, emp_image = request.POST.get('name2'), request.FILES['userimage']
        custom_user = CustomUser.objects.get(id = emp_id)
        # Image is encoded using calculate_face_encoding method
        en_image = str(emp_image)
        image_path = f'/home/dell/images/{en_image}'
        encod_image = calculate_face_encoding(image_path)
        AttendanceModel.objects.create(emp = custom_user,image = emp_image,encod_image  = encod_image)
        return redirect('/attendance/home')


class DataCollection(APIView):

	def get(self, request, format=None):
		snippets = AttendanceModel.objects.all()
		serializer = AttendanceSerializer(snippets, many=True)
		return Response(serializer.data)


def formatted_time(ele):
    ''' Returns the formatted time and date '''
    num = ele.rfind('(')
    ele2, ele3 = ele[:num - 1], ele[num+1:len(ele)-1]
    date_obj = datetime.datetime.strptime(ele2, '%d-%b-%Y').date()
    time_obj = datetime.datetime.strptime(ele3, '%H:%M:%S.%f').time()
    time_obj2 = time_obj.strftime("%I:%M %p")
    return time_obj, time_obj2, date_obj


def user_attendance_update(obj3, time_obj, time_obj2):
    ''' Updates the time out and work Status of the employees attendance record '''
    t2 = datetime.datetime.strptime(obj3[0].time_in, '%I:%M %p')
    t3 = datetime.timedelta(hours = time_obj.hour,minutes = time_obj.minute) - datetime.timedelta(hours = t2.hour, minutes = t2.minute)
    if t3 >= datetime.timedelta(hours = 4) and t3 <= datetime.timedelta(hours = 5):
        obj3.update(time_out = time_obj2, work_status = "Half Day Working")
    elif t3 >= datetime.timedelta(hours = 7) and t3 <= datetime.timedelta(hours = 10):
        obj3.update(time_out = time_obj2, work_status = "Full Day Working")
    else:
        pass


def weekday_attendance_record(date_obj, nm):
    ''' Updates the weekend record of employee '''
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
    ''' Updates the holiday record of employee '''
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


def get_dates(week, month, year=2021):
    return calendar.monthcalendar(year,month)[week]


def filter_attendance_name(request):
    ''' Filter attendance name according to their UserHeirarchy'''
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
    ''' Returns a list of objects according to their designation'''
    Web = [ele for ele in context['Web'] if ele in context1]
    DIR = [ele for ele in context['DIR'] if ele in context1]
    TL  = [ele for ele in context['TL']  if ele in context1]
    PM  = [ele for ele in context['PM'] if ele in context1]
    CTO = [ele for ele in context['CTO'] if ele in context1]
    return {'Web': Web, 'DIR': DIR, 'TL':TL, 'PM': PM, 'CTO': CTO}




class AttendanceInfo(DetailView):
    template_name = 'attendance/attendance_form.html'

    def get(self, request, *args, **kwargs):
        context =  display_empname()
        context1 = filter_attendance_name(request)
        data = attendance_form_filter(context, context1)
        # onelink, multilink = filter_channel_names(request)
        # mydict = {'onelink': onelink, 'multilink': multilink}
        return render(request, self.template_name, data)



def load_names(request):
    ''' AJAX function so that user can display attendance record weekly '''
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
    obj4 = DatewiseData.objects.filter(id__in = week_data)

    # Filtering the records yearly
    obj5 = [ele.id for ele in obj4 if ele.date.year == int(request.GET.get('year'))]
    obj6 = DatewiseData.objects.filter(id__in = obj5).order_by('date')

    # Converting the record in list data type
    obj7 = list(obj6.values())

    return JsonResponse(obj7, safe=False)


def load_names_monthly(request):
    ''' Function to display user's attendance record monthly '''
    name, week, month = request.GET.get('name'), request.GET.get('week'), request.GET.get('month')
    tup = []
    obj1 = DatewiseData.objects.filter(name = name[:name.rfind('@')])

    # Filter data monthly as per individual user
    for ele in obj1:
        if ele.date.month == int(month):
            tup.append(ele.id)
    obj2 = DatewiseData.objects.filter(id__in = tup)

    # Filtering the attendance record yearly 
    obj3 = [ele.id for ele in obj2 if ele.date.year == int(request.GET.get('year'))]
    obj4 = DatewiseData.objects.filter(id__in = obj3).order_by('date')

    # Converting the record in list data type
    obj5 = list(obj4.values())

    return JsonResponse(obj5, safe=False)



def mail_for_leave(subject, message, email_from, recipient_list):
    send_mail(subject, message, email_from, recipient_list)



class DayoffForm(FormView):
    template_name = 'attendance/dayoff_form.html'

    def get(self, request, *args, **kwargs):
        onedict = display_empname()
        # onelink, multilink = filter_channel_names(request)
        # mydict = {'onelink': onelink, 'multilink': multilink}
        return render(request, self.template_name, onedict)

    def post(self, request, *args, **kwargs):
        username = request.user.email
        name = username[:username.rfind('@')]
        calen1, calen2 =  request.POST.get('calen1'), request.POST.get('calen2')
        rec1, rec2 = request.POST.get('hr'), request.POST.get('tl')

        # Retreiving a record from CustomUser
        recp1 = CustomUser.objects.get(email = rec1)
        recp2 = CustomUser.objects.get(email = rec2)
        sender = CustomUser.objects.get(email = username)

        # Creating a attendance record of employee
        UserDayoffData.objects.create(
                                  name = name,
                                  leave_request_date = calen1,
                                  leave_from = calen1,
                                  leave_to = calen2,
                                  hr_approval = "Pending",
                                  tl_approval = "Pending",
                                  leave_reason = request.POST['reason']
                               )

        # Sending notification to the Tl or PM 
        message = str(calen1) +'@'+ str(calen2)
        data = str(sender)+" wants to take leave from "+str(calen1)+" to "+str(calen2)+" because "+ request.POST['reason']
        notify.send(sender = sender, 
                    recipient = recp2, 
                    verb = message, 
                    description = data,
                    action_object = recp1)

        # Sending email to tl and hr
        subject = 'Leave Request'
        message = data
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [rec2, rec1]
        mail_for_leave(subject, message, email_from, recipient_list)
        return redirect('/attendance/dayoff/success')



class LeaveFormSuccess(TemplateView):
    ''' Function ensuring that Request have been sent successfully by displaying this message'''
    template_name = 'attendance/leave_success.html'


class NotificationsPage(ListView):
    ''' This function display the notifications '''
    template_name = 'attendance/notifications.html'

    def get(self, request, *args, **kwargs):
        data = request.user.notifications.unread()
        # onelink, multilink = filter_channel_names(request)
        return render(request, 'attendance/notifications.html', {'data': data})



def not_object(obj, id1):
    ''' This function filter the particular object of notification ''' 
    for i in obj:
        if i.id == id1:
            mydata = {'des':i.description, 'verb': i.verb, 'actor': i.actor, 'recipient': i.recipient,
                        'id': i.id, 'recipient_id': i.recipient_id, 'action_object': i.action_object,
                        'timestamp': i.timestamp}    
    return mydata


def delete_not_object(obj, id1):
    ''' Makes the particular object of notifications as read '''
    for i in obj:
        if i.id == id1:
            i.mark_as_read()


class DeleteNot(View):

    def get(self, request, id1):
        ''' Makes the particular object of notifications as read '''
        obj = request.user.notifications.unread()
        for i in obj:
            if i.id == id1:
                i.mark_as_read()
        return redirect('/attendance/notifications_page')


            

class TlLeave(DetailView):
    template_name = 'attendance/tl_leave.html'

    def get(self, request, id, **kwargs):
        ''' Displaying the particular notifications of TL/PM '''
        obj = request.user.notifications.unread()
        mydata = not_object(obj, id)
        return render(request, 'attendance/tl_leave.html', mydata)



def tl_leave_approve(request,  id1, id2):
    ''' This is a AJAX function and this will call when the TL/PM will approve the 
          leave request. '''
    data = request.user.notifications.unread()
    user = CustomUser.objects.get(pk = id2)
    obj = user.notifications.unread()
    mydata = not_object(obj, id1)

    date1 = mydata['verb'][:mydata['verb'].rfind('@')]
    date2 = mydata['verb'][mydata['verb'].rfind('@') + 1:]

    # Updating the attendance record as Approved and timestamp
    object1 = UserDayoffData.objects.get(name = mydata['actor'], leave_from = date1)
    object1.tl_approval = 'Approved'
    object1.leave_request_date = mydata['timestamp']
    object1.save()

    # Sending notifications to HR or CTO after receiving by TL or PM
    object2 = CustomUser.objects.get(email = request.user.email)
    sender = CustomUser.objects.get(email = mydata['actor'])
    recp2 = CustomUser.objects.get(email = mydata['action_object'])
    data1 = str(sender)+" wants to take leave from "+str(date1)+" to "+str(date2)+" because "+ str(object1.leave_reason) +" and  approved by "+str(request.user.email)
    notify.send(sender = sender,
                recipient = recp2,
                verb = mydata['verb'],
                description = data1)

    # Sending notifications to the user who requests for leave
    data2 = str(object2)+" Approved your Leave Request"
    notify.send(sender = object2,
               recipient = sender,
               verb = "Response "+ mydata['verb'],
               description = data2)

    # Unread the particular object of notification
    delete_not_object(obj, id1)

    return render(request, 'attendance/notifications.html', {'data': data})



def tl_leave_not_approve(request, id1, id2):
    ''' This is a AJAX function and this will call when the TL/PM will not approve the 
          leave request. '''
    data = request.user.notifications.unread()
    user = CustomUser.objects.get(pk = id2)
    obj = user.notifications.unread()
    mydata = not_object(obj, id1)

    date1 = mydata['verb'][:mydata['verb'].rfind('@')]
    date2 = mydata['verb'][mydata['verb'].rfind('@') + 1:]

    object2 = CustomUser.objects.get(email = request.user.email)

    # Updating the attendance record as Approved and timestamp
    object1 = UserDayoffData.objects.get(name = mydata['actor'], leave_from = date1)
    object1.tl_approval = 'Not Approved'
    object1.leave_request_date = mydata['timestamp']
    object1.save()
    sender = CustomUser.objects.get(email = mydata['actor'])
    recp2 = CustomUser.objects.get(email = mydata['action_object'])
    data1 = str(sender)+" wants to take leave from "+str(date1)+" to "+str(date2)+" but not approved by "+str(request.user.email)

    # Sending notification to the HR or CTO
    notify.send(sender = sender, 
                recipient = recp2, 
                verb = mydata['verb'],
                description = data1)

    # Sending notification to the user who requested for leave
    data2 = str(object2)+" Not Approved your Leave Request"
    notify.send(sender = object2,
               recipient = sender,
               verb = "Response "+ mydata['verb'],
               description = data2)

    # Unread the particular object of notification
    delete_not_object(obj, id1)

    return render(request, 'attendance/notifications.html', {'data': data})



def hr_leave_approve(request, id1, id2):
    ''' This is a AJAX function and this will call when the CTO/HR will approve the 
          leave request. '''
    data = request.user.notifications.unread()
    user = CustomUser.objects.get(pk = id2)
    obj = user.notifications.unread()
    mydata = not_object(obj, id1)


    date1 = mydata['verb'][:mydata['verb'].rfind('@')]
    date2 = mydata['verb'][mydata['verb'].rfind('@') + 1:]

    # Updating the attendance record as Approved and timestamp
    object1 = UserDayoffData.objects.get(name = mydata['actor'], leave_from = date1)
    object1.hr_approval = 'Approved'
    object1.save()

    # Creating a attendance record of user as Dayoff
    date_obj1 = datetime.datetime.strptime(date1, '%Y-%m-%d').date()
    date_obj2 = datetime.datetime.strptime(date2, '%Y-%m-%d').date()
    date_diff = datetime.timedelta(days = date_obj2.day) - datetime.timedelta(days = date_obj1.day)
    num = 0
    if date_diff.days == 0:
        DatewiseData.objects.create(
                        name = mydata['actor'].username[:mydata['actor'].username.rfind('@')],
                        date = date_obj1,
                        week = calendar.day_name[date_obj1.weekday()],
                        time_in  = "-----",
                        time_out = "-----",
                        work_status = 'Leave'
                        )

    for i in range(0,date_diff.days + 1):
        mydate = date_obj1.day + num
        DatewiseData.objects.create(
                                name = mydata['actor'].username[:mydata['actor'].username.rfind('@')],
                                date = datetime.date(2021, date_obj1.month, mydate),
                                week = calendar.day_name[datetime.date(2021, 3, mydate).weekday()],
                                time_in  = "-----",
                                time_out = "-----",
                                work_status = 'Leave'
                            )
        num = num + 1

    # Sending notification to the user who requested for leave
    object2 = CustomUser.objects.get(email = request.user.email)
    data2 = str(object2)+" Approved your Leave Request"
    recp = CustomUser.objects.get(email = mydata['actor'])
    notify.send(sender = object2,
               recipient = recp,
               verb = "Response "+ mydata['verb'],
               description = data2)

    subject = 'Leave Request Accepted'
    message = "Your Leave Request have been approved by both "+str(request.user.email)+ " and your Tech Lead"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [mydata['actor']]
    mail_for_leave(subject, message, email_from, recipient_list)

    # Making a particular notification object as read
    delete_not_object(obj, id1)

    return render(request, 'attendance/notifications.html', {'data': data})



class HrLeave(UpdateView):
    template_name = 'attendance/hr_leave.html'

    def hr_leave(request, id1):
        ''' Displaying the particular notifications of HR/ CTO '''
        obj = request.user.notifications.unread()
        mydata = not_object(obj, id1)
        return render(request, self.template_name, mydata)




def hr_not_approve(request, id1, id2):
    ''' This is a AJAX function and this will call when the CTO/HR will NOT approve the 
          leave request. '''
    data = request.user.notifications.unread()
    user = CustomUser.objects.get(pk = id2)
    obj = user.notifications.unread()
    mydata = not_object(obj, id1)

    date1 = mydata['verb'][:mydata['verb'].rfind('@')]
    date2 = mydata['verb'][mydata['verb'].rfind('@') + 1:]

    # Updating the attendance record as Approved and timestamp
    object1 = UserDayoffData.objects.get(name = mydata['actor'], leave_from = date1)
    object1.hr_approval = 'Not Approved'
    object1.save()

     # Sending notification to the user who requested for leave
    object2 = CustomUser.objects.get(email = request.user.email)
    recp = CustomUser.objects.get(email = mydata['actor'])
    data2 = str(object2)+" Not Approved your Leave Request"
    notify.send(sender = object2,
                recipient = recp,
                verb = "Response "+ mydata['verb'],
                description = data2)

    # Making a particular notification object as read
    delete_not_object(obj, id1)

    return render(request, 'attendance/notifications.html', {'data': data})




class RemoveHoliday(UpdateView):
    ''' This function will call when particular holiday object have been delete '''
    def get(self, request, pk):
        obj1 = HolidayData.objects.get(id = pk)
        obj1.delete()
        return redirect('/attendance/holidays')



class HolidayDisplay(ListView):
    template_name = 'attendance/holiday.html'

    def get(self, request, *args, **kwargs):
        data = HolidayData.objects.all()
        # onelink, multilink = filter_channel_names(request)
        return render(request, self.template_name, {'data': data})

    def post(self, request, *args, **kwargs):
        data = HolidayData.objects.all()
        onelink, multilink = filter_channel_names(request)
        HolidayData.objects.create(
                            date = request.POST.get('calen1'),
                            occasion = request.POST.get('occassion')
                            )
        subject = 'Holiday Alert'
        message = """ On occassion of """+str(request.POST['occassion'])+ """ there is holiday tomorrow .
         Let your client's be informed. Have a good time , """+str(request.POST['occassion'])+""" to all
         in advance.
         """
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ["anushtha.shree321@gmail.com", "alban.shhai32@gmail.com"]

        date_obj1 = datetime.datetime.strptime(request.POST['calen1'], '%Y-%m-%d').date()

        time_diff = date_obj1 - datetime.date.today()
        if time_diff ==  datetime.timedelta(1):
            mail_for_leave(subject, message, email_from, recipient_list)
        return render(request, self.template_name, {'onelink': onelink, 'multilink': multilink, 'data': data})



class LeaveInfo(DetailView):
    ''' This function will display leave information of a particular employee '''
    template_name = 'attendance/leaveinfo.html'

    def get(self, request, *args, **kwargs):
        obj1 = UserDayoffData.objects.filter(name = request.user.username).exclude(hr_approval = 'Not Approved', tl_approval = 'Not Approved').order_by('-leave_to')
        # onelink, multilink = filter_channel_names(request)
        return render(request, self.template_name, {'data': obj1})



def start_button_status(request):
    obj1 = TimeSheetData.objects.filter(user_id = request.user.id,
                                        date = datetime.datetime.now())
    if obj1:
        if obj1[0].finish_time == '':
            return {'Start': "True", "Finish": ""}
        else:
            return {'Start': "True", "Finish": "True"}
    return {'Start': "", "Finish": ""}



class StartTime(CreateView):

    def get(self, request):
        obj1 = CustomUser.objects.get(id = request.user.id)
        start_tm = str(datetime.datetime.now().time())[:8]

        nm = CustomUser.objects.get(email = request.user.email)
        obj2 = TimeSheetData.objects.filter(user_id = nm,
                                            date = datetime.datetime.now()
                                            )

        if not obj2:
            TimeSheetData.objects.create(user_id = obj1,
                                     name = request.user.first_name +" "+ request.user.last_name,
                                     start_time = start_tm,
                                     )
        return redirect('/timesheet/record')



class FinishTime(UpdateView):

    def get(self, request):
        current_time = datetime.datetime.now()
        obj2 = CustomUser.objects.get(id = request.user.id)
        obj3 = TimeSheetData.objects.get(
                                        user_id = obj2,
                                        date = datetime.datetime.now(),
                                        )
        obj3.finish_time = str(datetime.datetime.now().time())[:8]
        start_tm = datetime.datetime.strptime(str(obj3.start_time), "%H:%M:%S").time()
        t1 = datetime.timedelta(hours = current_time.hour, minutes = current_time.minute)
        t2 = datetime.timedelta(hours = start_tm.hour, minutes = start_tm.minute)
        time_diff = t1 - t2
        obj3.total_time = str(datetime.datetime.strptime(str(time_diff), "%H:%M:%S").time())
        obj3.save()
        return redirect('/timesheet/record')


        
class TimeSheetRecord(DetailView):
    template_name = 'attendance/timesheet_record.html'

    def get(self, request, *args, **kwargs):
        context =  display_empname()
        context1 = filter_attendance_name(request)
        data = attendance_form_filter(context, context1)
        btndict = start_button_status(request)
        mydata = {**data, **btndict}
        onelink, multilink = filter_channel_names(request)
        mydict = {'onelink': onelink, 'multilink': multilink}
        return render(request, self.template_name, {**mydata, **mydict})



def record_updation(obj6):
    current_time = datetime.datetime.now()
    for ob in obj6:
        if ob.finish_time == '':
            # obj1 = TimeSheetData.objects.get(id = ob.id)
            start_tm = datetime.datetime.strptime(str(ob.start_time), "%H:%M:%S").time()
            t1 = datetime.timedelta(hours = current_time.hour, minutes = current_time.minute)
            t2 = datetime.timedelta(hours = start_tm.hour, minutes = start_tm.minute)
            time_diff = t1 - t2
            ob.total_time = str(datetime.datetime.strptime(str(time_diff), "%H:%M:%S").time())
            ob.save()
    return obj6



def emp_timesheet_record(request):
    name, week, month = request.GET.get('name'), request.GET.get('week'), request.GET.get('month')
    tup = []
    nm = CustomUser.objects.get(email = name)
    obj3 = TimeSheetData.objects.filter(user_id = nm)

    # Filter data monthly as per individual user
    for ele in obj3:
        if ele.date.month == int(month):
            tup.append(ele.id)
    obj4 = TimeSheetData.objects.filter(id__in = tup)

    # Filtering the attendance record yearly 
    obj5 = [ele.id for ele in obj4 if ele.date.year == int(request.GET.get('year'))]
    obj6 = TimeSheetData.objects.filter(id__in = obj5).order_by('date')
    obj7 = record_updation(obj6)
    # obj7 = TimeSheetData.objects.filter(id__in = obj5).order_by('date')

    # Converting the record in list data type
    obj8 = list(obj7.values())
    return JsonResponse(obj8, safe=False)








