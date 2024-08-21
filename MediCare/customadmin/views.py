import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import io
import urllib, base64
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from customadmin.backend import AdminBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .form import DoctorForm, AdminProfileForm, MedicalPreventationForm  
from base.models import Doctor, Admin, Medical_Preventation, Feedback, Patient, Heart_Patient, Diabetes_Patient, Parkinsons_Patient
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from django.db.models import Count


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = AdminBackend().authenticate(request, username=username, password=password)

            if user is not None and hasattr(user, 'Admin_ID'):
                # login(request, user)
                request.session['Admin_ID'] = user.Admin_ID
                messages.success(request, f'Welcome, {username}!')
                print("Admin_ID:", request.session.get('Admin_ID'))
                return redirect('dashboard') 
            else:
                messages.error(request, 'Invalid username or password.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    return render(request, 'C-admin/adlogin.html')

def custom_logout(request):
    if 'Admin_ID' in request.session:
        del request.session['Admin_ID']
    request.session.flush() 
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')

def add_doctor(request):
    form = DoctorForm()
    doctors = Doctor.objects.all().order_by('-Doctor_ID')
    
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            admin_id = request.session.get('Admin_ID')
            if admin_id is not None:
                try:
                    with transaction.atomic():
                        doctor = form.save(commit=False)
                        try:
                            admin = Admin.objects.get(pk=admin_id)
                            doctor.Admin_ID = admin
                            doctor.save()
                            messages.success(request, 'Doctor created successfully.')
                            return redirect('add_doctor')
                        except ObjectDoesNotExist:
                            messages.error(request, 'Admin not found.')
                except Exception as e:
                    messages.error(request, f'An error occurred: {str(e)}')
            else:
                messages.error(request, 'Admin ID not found in session.')
        else:
            print(form.errors) 
            messages.error(request, 'Form is not valid.')

    return render(request, 'C-admin/add_doctor.html', {'form': form, 'doctors': doctors})

def update_doctor(request, doctor_id):
    try:
        doctor = get_object_or_404(Doctor, pk=doctor_id)
    except ObjectDoesNotExist:
        messages.error(request, 'Doctor not found.')
        return redirect('add_doctor')

    context = {}  # Define context variable here

    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            admin_id = request.session.get('Admin_ID')
            if admin_id is not None:
                try:
                    with transaction.atomic():
                        doctor = form.save(commit=False)
                        doctor.Admin_ID_id = admin_id  # Assign the Admin instance ID directly to the Doctor's Admin_ID field
                        doctor.save()
                    messages.success(request, 'Doctor updated successfully.')
                    return redirect('add_doctor')
                except Exception as e:
                    messages.error(request, f'An error occurred: {str(e)}')
            else:
                messages.error(request, 'Admin ID not found in session.')
        else:
            messages.error(request, 'Form is not valid.')
    else:
        form = DoctorForm(instance=doctor)  # Pre-populate the form with existing data
        doctors = Doctor.objects.all().order_by('-Doctor_ID')
        context = {'form': form, 'doctors': doctors, 'Doctor_ID': doctor.Doctor_ID}

    return render(request, 'C-admin/add_doctor.html', context)

def delete_doctor(request, doctor_id):
    try:
        doctor = get_object_or_404(Doctor, pk=doctor_id)
    except ObjectDoesNotExist:
        messages.error(request, 'Doctor not found.')
        return redirect('add_doctor')

    if request.method == 'POST':
        if 'confirm_delete' in request.POST:  # Check for hidden form field
            try:
                with transaction.atomic():
                    doctor.delete()
                messages.success(request, 'Doctor deleted successfully.')
                return redirect('add_doctor')  # Redirect back to add_doctor (can be changed)
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
                return redirect('update_doctor', doctor.Doctor_ID)  # Redirect back to update on error
        else:
            messages.error(request, 'Delete confirmation not received.')
            return redirect('update_doctor', doctor.Doctor_ID)  # Redirect back to update on missing confirmation

    return render(request, 'delete_doctor_confirmation.html', {'doctor': doctor})

def dashboard(request):
    if 'Admin_ID' in request.session:
        admin_id = request.session['Admin_ID']
        patient_count = Patient.objects.count() 
        feedback_count = Feedback.objects.count()
        doctor_count = Doctor.objects.count()

        if 'view_count' not in request.session:
            request.session['view_count'] = 0

        # Increment the view count
        request.session['view_count'] += 1

        prediction_count = Heart_Patient.objects.count() + Diabetes_Patient.objects.count() + Parkinsons_Patient.objects.count()
        heart_disease_count = Heart_Patient.objects.count()
        diabetes_count = Diabetes_Patient.objects.count()
        parkinsons_count = Parkinsons_Patient.objects.count()  

        # Retrieve all cities and count the number of users for each city
        city_data = Patient.objects.values('Patient_Address').annotate(count=Count('Patient_Address')).order_by('Patient_Address')

        # Convert the queryset to a dictionary
        city_data_dict = {entry['Patient_Address']: entry['count'] for entry in city_data}
        print(city_data_dict)

        # Convert dictionary to JSON string
        city_data_json = json.dumps(city_data_dict)

        context = {
            'patient_count': patient_count,
            'feedback_count': feedback_count,
            'view_count': request.session['view_count'],
            'doctor_count': doctor_count,
            'heart_disease_count': heart_disease_count,
            'diabetes_count': diabetes_count,
            'parkinsons_count': parkinsons_count,
            'prediction_count': prediction_count,
            'city_data_json': city_data_json,
        }

        return render(request, 'C-admin/index.html', context)
    else:
        return redirect('login')
        
def login(request):
    return render(request, 'C-admin/Adlogin.html')

def delete_doctor_confirmation(request):
    return render(request, 'C-admin/delete_doctor_confirmation.html')

def get_topbar(request):
    admin_id = request.session.get('Admin_ID')
    admin = Admin.objects.get(pk=admin_id) if admin_id else None
    context = {'admin': admin}
    return render(request, 'C-admin/topbar.html', context)

def fpassword(request):
    return render(request, 'C-admin/forgot-password.html')

def reset_password(request):
    return render(request, 'C-admin/reset_password.html')

def forgot_password(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if Admin.objects.filter(Admin_Name=name).exists():
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid name. Please enter a valid name.')
    return render(request, 'C-admin/forgot-password.html')

def forgot_password(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the name exists in the database
        if Admin.objects.filter(Admin_Name=name).exists():
            # Check if the password and confirm password match
            if password == confirm_password:
                # Update the password in the database
                admin = Admin.objects.get(Admin_Name=name)
                admin.Admin_Password = password
                admin.save()
                messages.success(request, 'Password has been changed')
                # Redirect to a success page or login page
                return redirect('login')  # Redirect to login page
            else:
                # Password and confirm password don't match, show error message
                messages.error(request, 'Passwords do not match.')
        else:
            # Name does not exist, show error message
            messages.error(request, 'Invalid name. Please enter a valid name.')

    return render(request, 'C-admin/forgot-password.html')

def adprofile(request):
    admin_id = request.session.get('Admin_ID')
    admin = Admin.objects.get(pk=admin_id) if admin_id else None

    if request.method == 'POST':
        form = AdminProfileForm(request.POST, request.FILES, instance=admin)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('Edit_Profile')
    else:
        form = AdminProfileForm(instance=admin)
    return render(request, 'C-admin/Profile.html', {'form': form, 'admin': admin})

def trainM(request):
    return render(request, 'C-admin/Train.html')

def train_model(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        if csv_file.name.endswith('.csv'):
            fs = FileSystemStorage()
            filename = fs.save(csv_file.name, csv_file)
            file_path = os.path.join(fs.location, filename)
            data = pd.read_csv(file_path, encoding='latin1')
            
            # Search for possible columns that might represent the target variable
            possible_target_columns = ['target', 'outcome', 'status']  # Add more if needed
            
            # Try to find the first available column in the DataFrame
            target_column = None
            for col in possible_target_columns:
                if col in data.columns:
                    target_column = col
                    break
            
            if target_column is None:
                os.remove(file_path)
                return HttpResponse('No target variable found in the CSV file.')
            
            # Drop the target column from features
            X = data.drop(columns=[target_column])
            
            # Set y to the target column
            y = data[target_column]
            
            # Apply over-sampling
            ros = RandomOverSampler(random_state=0)
            X_resampled, y_resampled = ros.fit_resample(X, y)
            
            # Apply under-sampling
            rus = RandomUnderSampler(random_state=0)
            X_resampled, y_resampled = rus.fit_resample(X_resampled, y_resampled)
            
            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)
            
            # Train the model
            model = BernoulliNB()
            model.fit(X_train, y_train)
            
            # Evaluate the model
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            # Format accuracy as a percentage
            accuracy_percentage = round(accuracy * 100)
            
            # Pass accuracy and image URI to template
            return render(request, 'C-admin/Accuracy.html', {'accuracy': accuracy_percentage})
        else:
            return HttpResponse('Please upload a CSV file.')
    else:
        return HttpResponse('No file uploaded.')

def prevention(request):
    medical = Medical_Preventation.objects.all().order_by('-MP_ID')
    return render(request, 'C-admin/Medical_Pre.html',{'medical': medical})

def medical_preventation(request):
    if request.method == 'POST':
        form = MedicalPreventationForm(request.POST, request.FILES)
        if form.is_valid():
            admin_id = request.session.get('Admin_ID')
            if admin_id is not None:
                instance = form.save(commit=False)
                instance.Admin_ID_id = admin_id
                instance.save()
                messages.success(request, 'Medical prevention added successfully.')
            else:
                messages.error(request, 'Admin ID not found in session.')
        else:
            messages.error(request, 'Form is not valid.')
    else:
        form = MedicalPreventationForm()

    medical = Medical_Preventation.objects.all().order_by('-MP_ID')
    return render(request, 'C-admin/Medical_Pre.html', {'form': form, 'medical': medical, 'medical_preventation': None})

def update_medical_preventation(request, mp_id):
    try:
        medical_preventation = get_object_or_404(Medical_Preventation, pk=mp_id)
    except ObjectDoesNotExist:
        messages.error(request, 'Medical prevention not found.')
        return redirect('medical_preventation')

    if request.method == 'POST':
        form = MedicalPreventationForm(request.POST, request.FILES, instance=medical_preventation)
        if form.is_valid():
            admin_id = request.session.get('Admin_ID')
            if admin_id is not None:
                try:
                    with transaction.atomic():
                        medical_preventation = form.save(commit=False)
                        medical_preventation.Admin_ID_id = admin_id
                        medical_preventation.save()
                    messages.success(request, 'Medical prevention updated successfully.')
                    return redirect('medical_preventation')
                except Exception as e:
                    messages.error(request, f'An error occurred: {str(e)}')
            else:
                messages.error(request, 'Admin ID not found in session.')
        else:
            messages.error(request, 'Form is not valid.')
    else:
        form = MedicalPreventationForm(instance=medical_preventation)

    medical = Medical_Preventation.objects.all().order_by('-MP_ID')
    return render(request, 'C-admin/Medical_Pre.html', {'form': form, 'medical': medical, 'medical_preventation': medical_preventation})


def delete_medical_preventation(request, mp_id):
    try:
        medical_preventation = get_object_or_404(Medical_Preventation, pk=mp_id)
    except ObjectDoesNotExist:
        messages.error(request, 'Medical prevention not found.')
        return redirect('prevention')

    if request.method == 'POST':
        try:
            with transaction.atomic():
                medical_preventation.delete()
            messages.success(request, 'Medical prevention deleted successfully.')
            return redirect('prevention')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    else:
        messages.error(request, 'Invalid request method.')

    # Fetch all medical prevention data
    medical = Medical_Preventation.objects.all().order_by('-MP_ID')

    # Render the same template where the table is displayed, passing the medical data
    return render(request, 'C-admin/Medical_Pre.html', {'medical': medical})

def feedback_list(request):
    feedbacks = Feedback.objects.all()
    context = {
        'feedbacks': feedbacks,
    }
    return render(request, 'C-admin/Feedback.html', context)

def patient_list(request):
    patients = Patient.objects.all()
    context = {
        'patients': patients,
    }
    return render(request, 'C-admin/Patients.html', context)
    
def one_disease(request):
    if 'Admin_ID' in request.session:
        admin_id = request.session['Admin_ID']

        prediction_count = Heart_Patient.objects.count() + Diabetes_Patient.objects.count() + Parkinsons_Patient.objects.count()
        heart_disease_count = Heart_Patient.objects.count()
        diabetes_count = Diabetes_Patient.objects.count()
        parkinsons_count = Parkinsons_Patient.objects.count()  
        
        context = {
            'heart_disease_count': heart_disease_count,
            'diabetes_count': diabetes_count,
            'parkinsons_count': parkinsons_count,
            'prediction_count': prediction_count,
        }
    
        return render(request, 'C-admin/Popular_disease.html', context)
    else:
        return redirect('login')

def user_distribution_by_city(request):
    city_data = Patient.objects.values('Patient_Address').annotate(count=Count('Patient_Address')).order_by('Patient_Address')

    city_data_dict = {entry['Patient_Address']: entry['count'] for entry in city_data}
    print(city_data_dict)

    city_data_json = json.dumps(city_data_dict)

    return render(request, 'C-admin/Regions.html', {'city_data_json': city_data_json})

