from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Patient)
admin.site.register(Admin)
admin.site.register(Doctor)
admin.site.register(Feedback)
admin.site.register(save_doctor)
admin.site.register(Parkinsons)
admin.site.register(Diabetes)
admin.site.register(Heart_Disease)
# admin.site.register(Patient_Symptoms)
# admin.site.register(Symptoms)
