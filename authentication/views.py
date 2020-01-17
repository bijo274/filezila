from django.shortcuts import render
from django import forms
from .models import User


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='password', min_length=8, widget=forms.PasswordInput)
    password2 = forms.CharField(label='re-password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'name', 'phone')

    def cleaned_password(self):
        pass1 = self.cleaned_data.get['password1']
        pass2 = self.cleaned_data.get['password2']

        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError('Password mismatch')

        return pass2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get['password1'])

        if commit:
            user.save()
        return user


class UserAdminForm:
    pass
