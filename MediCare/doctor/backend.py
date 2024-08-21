from django.contrib.auth.backends import ModelBackend
from base.models import Doctor

# DoctorBackend
class DoctorBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            doctor = Doctor.objects.get(Doctor_Name=username)
            if doctor.Doctor_Password == password:  # You might want to hash the passwords for security
                return doctor
            else:
                return None  # Incorrect password
        except Doctor.DoesNotExist:
            return None  # Doctor not found
        except Exception as e:
            # Log the exception or handle it appropriately
            return None  # Other exceptions
