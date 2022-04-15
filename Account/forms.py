from django import forms
from .models import InstituteAdminAccount, StudentAccount, TeacherAccount, UserAccount
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.conf import settings

# class UserAccountForm(forms.ModelForm):
#     class Meta:
#         model = UserAccount
#         fields = ('first_name', 'last_name', 'username', 'email', 'type', 'department')

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(settings.DEFAULT_CUSTOM_USER_PASSWORD)
#         if commit:
#             user.save()
#         return user

class InstituteAdminAccountCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = InstituteAdminAccount
        fields = ('email', 'username', 'institute',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_institute_admin = True
        if commit:
            user.save()
        return user


class InstituteAdminAccountChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = InstituteAdminAccount
        fields = ('email', 'password', 'is_active', 'is_institute_admin')

    def clean_password(self):
        return self.initial["password"]

class StudentAccountCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=False)

    class Meta:
        model = StudentAccount
        fields = ('email', 'username', 'first_name', 'last_name', 'institute', 
                    'contact_no', 'short_intro', 'bio', 'profile_image', 
                    'department', 'type', 'roll_no')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password("abcde12345")
        if self.cleaned_data["password1"] != '':
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class StudentAccountChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = StudentAccount
        fields = ('email', 'username', 'first_name', 'last_name', 'institute', 
                    'contact_no', 'short_intro', 'bio', 'profile_image', 
                    'department', 'type', 'roll_no', 'password', 'is_active',)

    def clean_password(self):
        return self.initial["password"]

class StudentAccountEditForm(forms.ModelForm):

    class Meta:
        model = StudentAccount
        fields = ('first_name', 'last_name', 
                    'contact_no', 'short_intro', 'bio', 'profile_image', 
                    'department', 'roll_no',)

    def clean_password(self):
        return self.initial["password"]

class TeacherAccountCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=False)

    class Meta:
        model = TeacherAccount
        fields = ('email', 'username', 'first_name', 'last_name', 'institute', 
                    'contact_no', 'short_intro', 'bio', 'profile_image', 
                    'department', 'type', 'employment_id')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password("abcde12345")
        if self.cleaned_data["password1"] != '':
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class TeacherAccountChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = TeacherAccount
        fields = ('email', 'username', 'first_name', 'last_name', 'institute', 
                    'contact_no', 'short_intro', 'bio', 'profile_image', 
                    'department', 'type', 'employment_id', 'password', 'is_active',)
    
    def clean_password(self):
        return self.initial["password"]
