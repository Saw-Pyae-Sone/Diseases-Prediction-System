from django import forms
from base.models import Doctor

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

        widgets = {
            'Doctor_Password': forms.PasswordInput(),
        }

class DoctorEditForm(forms.ModelForm):
    class Meta:
        model = Doctor
        exclude = ['Doctor_Password', 'Admin_ID']
