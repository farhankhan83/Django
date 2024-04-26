from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Student
import os
from pathlib import Path

class RegisterForm(UserCreationForm):
  email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address', 'required': True}))
  first_name = forms.CharField(label="First Name", max_length= 50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name', 'required': True}))
  last_name = forms.CharField(label="Last Name", max_length= 50,  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name', 'required': True}))
  address = forms.CharField(label="Address",max_length= 50,  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address', 'required': True}))
  city = forms.CharField(label="City/Town",max_length= 50,  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City/Town', 'required': True}))
  country = forms.CharField(label="Country",max_length= 50,  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country', 'required': True}))
  photo = forms.ImageField(
     label="Profile Image",
     widget=forms.FileInput(
        attrs={'class': 'form-control', 'placeholder': 'Profile Picture', 'required': True}))
  date_of_birth = forms.DateField(label="Date of Birth", widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Date of Birth', 'required': True, 'type': 'date'}))

  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'address', 'city', 'country', 'photo', 'date_of_birth', 'password1', 'password2') 

  def __init__(self, *args, **kwargs):
      super(RegisterForm, self).__init__(*args, **kwargs)

      self.fields['username'].widget.attrs['class'] = 'form-control'
      self.fields['username'].widget.attrs['placeholder'] = 'User Name'
      self.fields['username'].label = 'Username'

      self.fields['password1'].widget.attrs['class'] = 'form-control'
      self.fields['password1'].widget.attrs['placeholder'] = 'Password'
      self.fields['password1'].label = 'Enter Password'
      self.fields['password1'].help_text = '''
      <ul class="form-text text-muted small">
        <li>Your password should not closely resemble your other personal details.</li>
        <li>Ensure your password consists of a minimum of 8 characters.</li>
        <li>Make sure your password includes both letters and numbers, not just numeric digits.</li>
        <li>Avoid using passwords that are commonly used by others.</li>
      </ul>'''

      self.fields['password2'].widget.attrs['class'] = 'form-control'
      self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
      self.fields['password2'].label = 'Confirm Password'
      self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'



class UserStudentEditForm(UserChangeForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    date_of_birth = forms.DateField(label="Date of Birth", widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Date of Birth', 'required': True, 'type': 'date'}))
    address = forms.CharField(label="Address", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address', 'required': True}))
    city_town = forms.CharField(label="City/Town", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City/Town', 'required': True}))
    country = forms.CharField(label="Country", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country', 'required': True}))

    def __init__(self, *args, **kwargs):
        super(UserStudentEditForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].widget.attrs['readonly'] = True

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'

        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['password'].widget.attrs['hidden'] = True

    def save(self, commit=True):
        user = super().save(commit=False)
        student = user.student
        student.date_of_birth = self.cleaned_data['date_of_birth']
        student.address = self.cleaned_data['address']
        student.city_town = self.cleaned_data['city_town']
        student.country = self.cleaned_data['country']
        student.photo = student.photo
        if commit:
            user.save()
            student.save()
        return user