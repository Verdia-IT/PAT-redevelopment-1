from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile

from .forms import UserAdminChangeForm, UserAdminCreationForm
# Register your models here.

User = get_user_model()

class UserAdmin(BaseUserAdmin):    
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('email','admin')
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('email','password') }),
        # ('Personal info',{'fields': ('',)}),
        ('Permissions',{"fields": ('admin','staff','active')}),
    )

    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email','password1','password2') }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Profile)