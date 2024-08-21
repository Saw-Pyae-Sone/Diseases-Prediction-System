# from django.contrib import admin
from django.urls import path
from .views import Dindex, custom_Dlogin, Dabout, custom_Dlogout, doctor, Dhistory, Pheart_detail, Dprofile, dlogin, Pdiabetes_detail,  Pparkinsons_detail, Forgot_P, pforgot_password

urlpatterns = [
    path('doctor_index/', Dindex, name='Dindex'), 
    path('doctor_login/', dlogin, name="dlogin"),
    path('logging_in/', custom_Dlogin, name="custom_Dlogin"),
    path('About us/', Dabout, name="Dabout-us"),
    path('Logout/', custom_Dlogout, name="custom_Dlogout"),
    path('Doctors/', doctor, name="Ddoctors"),
    path('DHistory/', Dhistory, name="Dhistory"),
    path('heart_detailed/<int:hd_id>/',Pheart_detail, name='PHeart_Detailed'),
    path('diabetes_detailed/<int:dia_id>/', Pdiabetes_detail, name='ddiabetes_detailed'),
    path('Pparkinsons_detailed/<int:par_id>/', Pparkinsons_detail, name='Pparkinsons_detailed'),
    path('doctor_profile/', Dprofile, name="Dprofile"),
    path('Forgot_Password/', Forgot_P, name="Forgot_P"),
    path('pforgot_password/', pforgot_password, name="pforgot_password"),
]