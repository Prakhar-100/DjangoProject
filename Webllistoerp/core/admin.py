from django.contrib import admin
from .models import CustomUser, UserHeirarchy
from django.contrib.auth.admin import UserAdmin
from .forms import UserForm
# Register your models here.

# class UserModelAdmin(admin.ModelAdmin):
# 	list_display = ('first_name', 'last_name', 'email', 'designation', 'user_name', 'password', 'confirm_pass') 

# admin.site.register(UserHeirarchy)
@admin.register(UserHeirarchy)
class PostAdmin(admin.ModelAdmin):
	list_display = ['usernm', 'child']


class CustomUserAdmin(UserAdmin):
	model = CustomUser
	add_form = UserForm

# admin.site.register(UserModel)
# admin.site.register(ProfileModel)

admin.site.register(CustomUser, CustomUserAdmin)

fieldsets = (
	*UserAdmin.fieldsets,
	(
		'User Role',
		{
			'fields': (

					'designation',
				)
		}
	)
)

