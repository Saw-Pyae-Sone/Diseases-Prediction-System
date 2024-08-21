
from django import forms
from base.models import Doctor, Admin, Medical_Preventation

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['Doctor_Name', 'Doctor_Email', 'Doctor_Password', 'Doctor_Address', 'Doctor_Experience', 'Doctor_License', 'Doctor_Specialty', 'Doctor_Languages', 'Doctor_Image']
        widgets = {
            'Doctor_Password': forms.PasswordInput(),
        }

    # def save(self, commit=True):
    #     instance = super(DoctorForm, self).save(commit=False)
    #     doctor_image = self.cleaned_data.get('Doctor_Image')

    #     if doctor_image:
    #         instance.Doctor_Image = doctor_image 
    #     else:
    #         if self.fields['Doctor_Image'].required:
    #             self.add_error('Doctor_Image', "Doctor Image is required.") 
    #         else:
    #             instance.Doctor_Image = None
        
    #     if commit:
    #         instance.save()
        
    #     return instance

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['Admin_Name', 'Admin_Email', 'Admin_Image']

    def __init__(self, *args, **kwargs):
        super(AdminProfileForm, self).__init__(*args, **kwargs)
        self.fields['Admin_Name'].widget.attrs['readonly'] = True
        self.fields['Admin_Email'].widget.attrs['readonly'] = True 

class MedicalPreventationForm(forms.ModelForm):
    class Meta:
        model = Medical_Preventation
        fields = ['Medical_Image', 'Diseases']