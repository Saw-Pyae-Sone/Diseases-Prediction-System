from django.contrib.auth.backends import ModelBackend
from .models import Patient

class PatientBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            patient = Patient.objects.get(Patient_Email=email)
            if patient.Patient_Password == password:
                return patient
        except Patient.DoesNotExist:
            pass
        except Exception as e:
            pass

        return None
