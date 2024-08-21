from django.urls import path
from . import views
from .views import predict_heart

urlpatterns = [
    path('Home/',views.home, name="home"),
    path('Aboutus/', views.aboutus, name="about-us"),
    path('predict_heart/', views.predict_heart, name="predict_heart"),
    path('Diabetes/', views.diabetes, name='diabetes'),
    path('Parkinsons/', views.parkinsons, name='parkinsons'),
    path('Feedback/', views.feedback, name="feedback"),
    path('',views.index, name="index"),
    path('predict_diabetes/', views.predict_diabetes, name="predict_diabetes"),
    path('predict_parkinsons/', views.predict_parkinsons, name="predict_parkinsons"),
    path('plogin/', views.login, name="plogin"),
    path('doctors/', views.doctor, name="doctors"),
    path('register/', views.register, name="register"),
    path('add-patient/', views.register_patient, name="add_patient"),
    path('Logging_in/', views.custom_Plogin, name="custom_Plogin"),
    path('Logout/', views.custom_plogout, name="custom_plogout"),
    path('History/', views.History, name="History"),
    path('profile/', views.profile, name='profile'),
    path('edit_patient/', views.edit_patient, name='edit_patient'),
    path('feedback_add/', views.feedback_add, name="feedback_add"),
    path('heart_detail/<int:hd_id>/', views.heart_detail, name="Heart_Detailed"),
    path('save_doctor/<int:doctor_id>/', views.sdoctor, name='save_doctor'),
    path('remove_doctor/<int:doctor_id>/', views.remove_doctor, name='remove_doctor'),
    path('diabetes_detail/<int:dd_id>/', views.diabetes_detail, name='diabetes_detail'),
    path('parkinsons_detail/<int:par_id>/', views.parkinsons_detail, name='parkinsons_detail'),
    path('Forgot_Pass/', views.Forgot_P, name='PForgot_P'),
    path('Forgot_Password/', views.mforgot_password, name="mforgot_password"),
    path('Medical_Prevention/', views.mel_prevention, name="mel_prevention"),
]