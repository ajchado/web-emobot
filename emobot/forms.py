from django import forms
from django.db.models import fields
from django.db.models.base import Model
from .models import *

class PersonForm(forms.ModelForm):
	
	class Meta:
		model = Person
		fields = ('username','password', 'firstName', 'lastName', 'email', 'gender')

