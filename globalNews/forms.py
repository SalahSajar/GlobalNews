from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


class UserAccountSettingsForm(forms.Form):
    class Meta(ModelForm):
        model = User
        fields = '__all__'
