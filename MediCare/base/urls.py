from django.urls import path
from . import views
from .views import predict_heart

urlpatterns = [
    path('',views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('create-room/', views.createRoom, name="create-room"),
    path('Aboutus/', views.aboutus, name="about-us"),
    path('predict_heart/', views.predict_heart, name="predict_heart"),
    path('Diabetes/', views.diabetes, name='diabetes'),
    path('Parkinsons/', views.parkinsons, name='parkinsons'),
    path('Feedback/', views.feedback, name="feedback"),
    path('predict_diabetes/', views.predict_diabetes, name="predict_diabetes"),
    path('predict_parkinsons/', views.predict_parkinsons, name="predict_parkinsons"),
]