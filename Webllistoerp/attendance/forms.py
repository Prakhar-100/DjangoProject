from django import forms
from .models import DatewiseData,CustomUser

class AttendanceData(forms.Form):
	name = forms.CharField(max_length = 50,
		widget = forms.TextInput())
	image = forms.FileField()

MONTH_CHOICE_FIELD = [
          ('01','January'),
          ('02', 'Febuary'),
          ('03', 'March'),
          ('04', 'April'),
          ('05', 'May'),
          ('06', 'June'),
          ('07', 'July'),
          ('08', 'August'),
          ('09', 'September'),
          ('10', 'October'),
          ('11', 'November'),
          ('12', 'December')
          ]

WEEK_CHOICE_FIELD = [
         ('Sun', 'Sunday'),
         ('Mon', 'Monday'),
         ('Tue', 'Tuesday'),
         ('Wed', 'Wednesday'),
         ('Thurs', 'Thursday'),
         ('Fri', 'Friday'),
         ('Sat', 'Saturday')
          ]

class AttendanceInfo(forms.Form):

	name = forms.ModelChoiceField(label = "Employee Name",
		                  queryset = CustomUser.objects.all().order_by('id'))
	month = forms.CharField(max_length = 100, label = 'MONTHLY',
		                 widget=forms.Select(choices=MONTH_CHOICE_FIELD))
	week = forms.CharField(max_length = 100, label = 'WEEKLY',
		                 widget=forms.Select(choices=WEEK_CHOICE_FIELD))

CHOICES_APPROVE = [
      ('Approved','Approved'),
      ('Not Approved', 'Not Approved')
      ]

class DayoffForm(forms.Form):
  name = forms.CharField(max_length = 100)
  date = forms.DateField(widget = forms.DateInput())
  hr_approval = forms.ChoiceField(widget = forms.Select(choices = CHOICES_APPROVE))
  tech_lead_approval = forms.ChoiceField(widget = forms.Select(choices = CHOICES_APPROVE))
  dayoff_reason = forms.CharField(max_length = 500)

	


