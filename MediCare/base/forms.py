from django import forms
from .models import Patient, Feedback

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

        widgets = {
            'Patient_Password': forms.PasswordInput(),
        }

class PatientEditForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['Patient_Password']

    # def save(self, commit=True):
    #     instance = super(PatientForm, self).save(commit=False)
    #     patient_image = self.cleaned_data.get('Patient_Family_Medical_History')

    #     if patient_image:
    #         instance.Patient_Family_Medical_History = patient_image.name
    #     else:
    #         if self.fields['Patient_Family_Medical_History'].required:
    #             self.add_error('Patient_Family_Medical_History', "Family History is required.")
    #         else:
    #             instance.Patient_Family_Medical_History = None

    #     patient_image = self.cleaned_data.get('Patient_Image')

    #     if patient_image:
    #         instance.Patient_Image = patient_image.name
    #     else:
    #         if self.fields['Patient_Image'].required:
    #             self.add_error('Patient_Image', "Profile Picture is required.")
    #         else:
    #             instance.Patient_Image = None
        
    #     if commit:
    #         instance.save()
        
    #     return instance
    
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['Title', 'Message']
        exclude = ['Patient_ID']
