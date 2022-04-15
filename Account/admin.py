from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from Account.models import Account, StudentAccount, TeacherAccount, InstituteAdminAccount
from .forms import (InstituteAdminAccountCreationForm, InstituteAdminAccountChangeForm,
                    StudentAccountCreationForm, StudentAccountChangeForm,
                    TeacherAccountCreationForm, TeacherAccountChangeForm)


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_active')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ('date_joined',)
    fieldsets = ()
    ordering = ('-date_joined',)

    class Meta:
        model = Account

class InstituteAdminAccountAdmin(admin.ModelAdmin):
    change_form = InstituteAdminAccountChangeForm
    add_form = InstituteAdminAccountCreationForm
    list_display = ('email', 'username', 'institute', 'is_active')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ('date_joined',)
    fieldsets = ()
    ordering = ('-date_joined',)

    class Meta:
        model = InstituteAdminAccount

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = self.add_form
        else:
            self.form = self.change_form

        return super(InstituteAdminAccountAdmin, self).get_form(request, obj, **kwargs)

class StudentAccountAdmin(admin.ModelAdmin):
    change_form = StudentAccountChangeForm
    add_form = StudentAccountCreationForm
    list_display = ('email', 'username', 'institute',
                    'department', 'roll_no', 'is_active')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ('date_joined',)
    fieldsets = ()
    ordering = ('-date_joined',)

    class Meta:
        model = StudentAccount

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = self.add_form
        else:
            self.form = self.change_form

        return super(StudentAccountAdmin, self).get_form(request, obj, **kwargs)

class TeacherAccountAdmin(admin.ModelAdmin):
    change_form = TeacherAccountChangeForm
    add_form = TeacherAccountCreationForm
    list_display = ('email', 'username', 'institute',
                    'department', 'employment_id', 'is_active')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ('date_joined',)
    fieldsets = ()
    ordering = ('-date_joined',)

    class Meta:
        model = TeacherAccount

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = self.add_form
        else:
            self.form = self.change_form

        return super(TeacherAccountAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(Account, AccountAdmin)
admin.site.register(StudentAccount, StudentAccountAdmin)
admin.site.register(TeacherAccount, TeacherAccountAdmin)
admin.site.register(InstituteAdminAccount, InstituteAdminAccountAdmin)
admin.site.unregister(Group)