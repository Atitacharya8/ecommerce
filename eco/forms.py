from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from eco.models import Product, Category
from . import models



class ReviewForm(forms.ModelForm):
    class Meta:
        fields=["rate","review"]
        model=models.Review

class FeedbackForm(forms.ModelForm):
    class Meta:
        fields=["rate","feedback"]
        model=models.Feedback


class SigninForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)


class SignupForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]


class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields='__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields='__all__'


