from django import forms





class CallingForm(forms.Form):
	name = forms.CharField(max_length = 50)
	mob = forms.CharField(max_length = 20)
	