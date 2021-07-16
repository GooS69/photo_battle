from django.forms import ModelForm
from django import forms
from post.my_models.custom_user import CustomUser


class CustomUserAvatarForm(ModelForm):

    avatar = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['avatar']
