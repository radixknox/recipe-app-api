from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models
#Add you costom user model to the admin page...And make required changes
#costomization of django Admin
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email','name']
    fieldsets = (                                  #these fieldsets are for user_details(in admin) change page
        (None,{'fields': ('email','password')}),
        (_('Personel Info'),{'fields':('name',)}),
        (

            _('permissions'),
            {'fields':('is_staff','is_superuser','is_active')}
        ),
        (_('Important Dates'),{'fields':('last_login',)})
    )

    add_fieldsets = (
        (None,
        {
        'classes':('wide'),
        'fields' : ('email','password1','password2')
        }
        ),

    )

admin.site.register(models.User,UserAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)

# Register your models here.
