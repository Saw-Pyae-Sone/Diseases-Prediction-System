from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
    
class Patient(models.Model):
    Patient_ID = models.AutoField(primary_key = True)
    Patient_Name = models.CharField(max_length=200)
    Patient_Email = models.CharField(max_length=255)
    Patient_Password = models.CharField(max_length=255)
    Patient_Address = models.CharField(max_length=255)
    Patient_Image = models.ImageField(upload_to='patient_img/', null=True, blank=True)
    Patient_Family_Medical_History = models.ImageField(upload_to='medical_history/',null=True, blank=True)

    def __str__(self):
        return self.Patient_Name

class Admin(models.Model):
    Admin_ID = models.AutoField(primary_key = True)
    Admin_Name = models.CharField(max_length=200)
    Admin_Email = models.CharField(max_length=255)
    Admin_Password = models.CharField(max_length=200, default='admin123')
    Admin_Image = models.ImageField(upload_to='Admin_img/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.Admin_Name

class Doctor(models.Model):
    Doctor_ID = models.AutoField(primary_key = True)
    Doctor_Name = models.CharField(max_length=200)
    Doctor_Email = models.CharField(max_length=255)
    Doctor_Password = models.CharField(max_length=200)
    Doctor_Address = models.CharField(max_length=255)
    Doctor_Experience = models.CharField(max_length = 200)
    Doctor_License = models.CharField(max_length = 200)
    Doctor_Specialty = models.CharField(max_length = 255)
    Doctor_Languages = models.CharField(max_length = 255)
    Doctor_Image = models.ImageField(upload_to='cimg/', null=True, blank=True)
    Admin_ID = models.ForeignKey(Admin, on_delete=models.CASCADE)

    def __str__(self):
        return self.Doctor_Name

class Feedback(models.Model):
    Feedback_ID = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=200)
    Message = models.TextField()
    Patient_ID = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.Title

class save_doctor(models.Model):
    SD_ID = models.AutoField(primary_key=True)
    Patient_ID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    Doctor_ID = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __stf__(self):
        return f"SavedDoctor {self.SD_ID}"

class Parkinsons(models.Model):
    Par_ID = models.AutoField(primary_key=True)
    Par_Name = models.CharField(max_length = 255, default="Parkinsons")
    MDVP_FO_Hz = models.FloatField()
    MDVP_Fhi_Hz = models.FloatField()
    MDVP_Flo_hz = models.FloatField()
    MDVP_Jitter_percentage = models.FloatField()
    MDVP_Jibber_Abs = models.FloatField()
    MDVP_RAP = models.FloatField()
    MDVP_PPQ = models.FloatField()
    Jitter_DDP = models.FloatField()
    MDVP_Shimmer = models.FloatField()
    MDVP_Shimmer_dB = models.FloatField()
    Shimmer_APQ3 = models.FloatField()
    Shimmer_APQ5 = models.FloatField()
    MDVP_APQ = models.FloatField()
    Shimmer_DDA = models.FloatField()
    NHR = models.FloatField()
    HNR = models.FloatField()
    RPDE = models.FloatField()
    DFA = models.FloatField()
    spread1 = models.FloatField()
    spread2 = models.FloatField()
    D2 = models.FloatField()
    PPE = models.FloatField()
    status = models.IntegerField()

    def __str__(self):
        return str(self.status)

class Diabetes(models.Model):
    Dia_ID = models.AutoField(primary_key=True)
    Dia_Name = models.CharField(max_length = 255, default = "Diabetes")
    Diabetes_012 = models.IntegerField(default=0)
    HighBP = models.FloatField()
    HighChol = models.FloatField()
    CholCheck = models.FloatField()
    BMI = models.FloatField()
    Smoker = models.FloatField()
    Stroke = models.FloatField()
    HeartDiseaseorAttack = models.FloatField()
    PhysActivity = models.FloatField()
    Fruits = models.FloatField()
    Veggies = models.FloatField()
    HvyAlcoholConsump = models.FloatField()
    AnyHealthcare = models.FloatField()
    NoDocbcCost = models.FloatField()
    GenHlth = models.FloatField()
    MentHlth = models.FloatField()
    PhysHlth = models.FloatField()
    DiffWalk = models.FloatField()
    Sex = models.IntegerField()
    Age = models.IntegerField()
    Education = models.FloatField()
    Income = models.FloatField()

    def __str__(self):
        return self.HeartDiseaseorAttack

class Heart_Disease(models.Model):
    HD_ID = models.AutoField(primary_key=True)
    HD_Name = models.CharField(max_length = 255, default="Heart_diseases")
    age = models.IntegerField()
    sex = models.IntegerField()
    cp = models.IntegerField()
    trestbps = models.IntegerField()
    chol = models.IntegerField()
    fbs = models.IntegerField()
    restecg = models.IntegerField()
    thalach = models.IntegerField()
    exang = models.IntegerField()
    oldpeak = models.FloatField()
    slope = models.IntegerField()
    ca = models.IntegerField()
    thal = models.IntegerField()
    target = models.IntegerField()

    def __str__(self):
        return f"Heart Disease {self.HD_ID}"
    
class Heart_Patient(models.Model):
    Heart_Patient_ID = models.AutoField(primary_key=True)
    HD_ID = models.ForeignKey(Heart_Disease, on_delete=models.CASCADE)
    Patient_ID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    Heart_Percentages = models.FloatField()
    heart_prediction_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"Heart Patient {self.Heart_Patient_ID}"

class Diabetes_Patient(models.Model):
    Diabetes_Patient_ID = models.AutoField(primary_key=True)
    Dia_ID = models.ForeignKey(Diabetes, on_delete=models.CASCADE)
    Patient_ID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    Diabetes_Percentages = models.FloatField()
    diabetes_prediction_date = models.DateTimeField(default=timezone.now())

    def __stf__(self):
            return self.Diabetes_Patient_ID

class Parkinsons_Patient(models.Model):
    Parkinsons_Patient_ID = models.AutoField(primary_key=True)
    Par_ID = models.ForeignKey(Parkinsons, on_delete=models.CASCADE)
    Patient_ID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    Parkinsons_Percentages = models.FloatField()
    parkinsons_prediction_date = models.DateTimeField(default=timezone.now())

    def __stf__(self):
        return self.Parkinsons_Patient_ID

class Medical_Preventation(models.Model):
    MP_ID = models.AutoField(primary_key=True)
    Medical_Image = models.ImageField(upload_to='Medical/',null=True, blank=True)
    Diseases = models.CharField(max_length=255, default="Diabetes")
    Admin_ID = models.ForeignKey(Admin, on_delete=models.CASCADE)

    def __stf__(self):
        return self.MP_ID


