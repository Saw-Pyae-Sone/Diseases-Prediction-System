# # yourappname/backends.py
# from django.contrib.auth.backends import ModelBackend
# from base.models import Admin

# class AdminBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             admin = Admin.objects.get(Admin_Name=username)
#             if admin.Admin_Password == password:
#                 return admin
#         except Admin.DoesNotExist:
#             return None

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from base.models import Admin

class AdminBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            admin = Admin.objects.get(Admin_Name=username)
            # if check_password(password, admin.Admin_Password):
            if admin.Admin_Password == password:
                return admin
                # return {'user': admin, 'is_authenticated': True}
        except Admin.DoesNotExist:
            pass  # Don't reveal whether the user or password was incorrect
        except Exception as e:
            # Log the exception or handle it appropriately
            pass

        return None

