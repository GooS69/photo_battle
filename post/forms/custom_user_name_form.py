from django.forms import ModelForm
from django import forms
from post.my_models.custom_user import CustomUser


class CustomUserNameForm(ModelForm):

    class Meta:
        model = CustomUser
        fields = ['first_name', ]
