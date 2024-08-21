# from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', custom_login, name='custom_login'),  # Corrected URL name
    path('dashboard/', dashboard, name='dashboard'),  # Corrected URL name
    path('login/', login, name='login'),  # Corrected URL name
    path('add_doctor/', add_doctor, name='add_doctor'),
    path('logout/', custom_logout, name='custom_logout'),
    path('update_doctor/<int:doctor_id>/', update_doctor, name='update_doctor'),
    path('delete_doctor/<int:doctor_id>/', delete_doctor, name='delete_doctor'),
    path('delete_doctor_confirmation/<int:doctor_id>/', delete_doctor_confirmation, name='delete_doctor_confirmation'),
    path('fpassword', fpassword, name='fpassword'),
    path('forgot_password', forgot_password, name='forgot_password'),
    path('reset_password', reset_password, name="reset_password"),
    path('Profile/', adprofile, name='Edit_Profile'),
    path('train/', trainM, name='trainM'),
    path('train_model/', train_model, name='train_model'),
    path('prevention/', prevention, name="prevention"),
    path('medical_preventation/', medical_preventation, name="medical_preventation"),
    path('update_medical_preventation/<int:mp_id>/', update_medical_preventation, name="update_medical_preventation"),
    path('delete_medical_preventation/<int:mp_id>/', delete_medical_preventation, name="delete_medical_preventation"),
    path('feedback_list/', feedback_list, name="feedback_list"),
    path('patients/', patient_list, name='patient_list'),
    path('Diseases/', one_disease, name='one_disease'),
    path('Regions/', user_distribution_by_city, name="Regions")
]