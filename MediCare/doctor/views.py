from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from base.models import Doctor, Heart_Disease, save_doctor, Diabetes_Patient, Parkinsons_Patient, Heart_Patient, Patient, Admin
from .backend import DoctorBackend
from django.http import HttpResponseBadRequest
from .forms import DoctorForm, DoctorEditForm

# Create your views here.
def Dindex(request):
    doctors = Doctor.objects.all()
    context = {'doctors': doctors}
    return render(request, 'Doctor/index.html', context)

def Dabout(request):
    doctors = Doctor.objects.all()
    context = {'doctors': doctors}
    return render(request, 'Doctor/about.html', context)

def doctor(request):
    doctors = Doctor.objects.all()
    context = {'doctors': doctors}
    return render(request, 'Doctor/doctors.html', context)

def dlogin(request):
    return render(request, 'Doctor/Login.html')

def custom_Dlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = DoctorBackend().authenticate(request, username=username, password=password)  # Fix parameter name

            if user is not None:
                # login(request, user)
                request.session['Doctor_ID'] = user.Doctor_ID  # Assuming 'id' is the primary key attribute
                messages.success(request, f'Welcome, {username}!')
                print("Doctor_ID:", request.session.get('Doctor_ID'))
                return redirect('Dindex') 
            else:
                messages.error(request, 'Invalid username or password.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    return render(request, 'Doctor/Login.html')

def custom_Dlogout(request):
    if 'Doctor_ID' in request.session:
        del request.session['Doctor_ID']
    request.session.flush() 
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('custom_Dlogin')
    
def Dprofile(request):
    if 'Doctor_ID' in request.session:
        doctor_id = request.session['Doctor_ID']
        try:
            doctor = Doctor.objects.get(pk=doctor_id)
        except Doctor.DoesNotExist:
            return redirect('Dprofile')

        if request.method == 'POST':
            form = DoctorEditForm(request.POST, request.FILES, instance=doctor)
            if form.is_valid():
                try:
                    admin = Admin.objects.get(pk=1)  # Fetch the Admin instance
                except Admin.DoesNotExist:
                    messages.error(request, 'Admin not found.')
                    return render(request, 'Doctor/Profile.html', {'form': form, 'doctor': doctor})
                
                doctor.Admin_ID = admin  # Assign the Admin instance
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('Dprofile')
            else:
                messages.error(request, 'Form is not valid. Please check the input data.')
                return render(request, 'Doctor/Profile.html', {'form': form, 'doctor': doctor})
        else:
            form = DoctorEditForm(instance=doctor)

        return render(request, 'Doctor/Profile.html', {'form': form, 'doctor': doctor})
    else:
        return redirect('login')  # Redirect if no doctor ID in session
    
def Dhistory(request):
    if 'Doctor_ID' in request.session:
        doctor_id = request.session['Doctor_ID']
        
        # Fetch the doctor object
        doctor = get_object_or_404(Doctor, pk=doctor_id)

        # Fetching saved patients for the logged-in doctor
        saved_patients = save_doctor.objects.filter(Doctor_ID=doctor_id).values_list('Patient_ID', flat=True)
        
        # Fetch complete patient objects
        patients = Patient.objects.filter(pk__in=saved_patients)

        # Initialize context with patients and doctor
        context = {
            'patients': patients,
            'doctor': doctor,  # Include doctor object in context
        }

        # Add condition based on doctor's specialization
        if doctor.Doctor_Specialty == 'Heart_diseases':
            dheart_disease_data = Heart_Patient.objects.filter(Patient_ID__in=saved_patients).select_related('Patient_ID')
            context['dheart_disease_data'] = dheart_disease_data
        elif doctor.Doctor_Specialty == 'Diabetes':
            ddiabetes_data = Diabetes_Patient.objects.filter(Patient_ID__in=saved_patients).select_related('Patient_ID')
            context['ddiabetes_data'] = ddiabetes_data
        elif doctor.Doctor_Specialty == 'Parkinsons':
            dparkinsons_data = Parkinsons_Patient.objects.filter(Patient_ID__in=saved_patients).select_related('Patient_ID')
            context['dparkinsons_data'] = dparkinsons_data
        else:
            # Optionally handle case where doctor's specialization is not recognized
            messages.error(request, 'Specialization not recognized.')

        return render(request, 'Doctor/History.html', context)
    else:
        return redirect('dlogin')


def Pheart_detail(request, hd_id):
    if 'Doctor_ID' in request.session:
        doctor_id = request.session['Doctor_ID']

        # Fetching saved patients for the logged-in doctor
        saved_patients = save_doctor.objects.filter(Doctor_ID=doctor_id).values_list('Patient_ID', flat=True)
        
        # Fetch complete patient objects
        patients = Patient.objects.filter(pk__in=saved_patients)

        # Fetching heart disease data for the specific HD_ID associated with the doctor
        dheart_disease_data = Heart_Patient.objects.filter(Patient_ID__in=saved_patients, HD_ID=hd_id).select_related('HD_ID', 'Patient_ID').first()

        return render(request, 'Doctor/Heart_Detailed.html', {
            'dheart_disease_data': dheart_disease_data,
            'patients': patients
        })
    else:
        return HttpResponseBadRequest('Doctor ID not found in session.')
    
def Pdiabetes_detail(request, dia_id):
    if 'Doctor_ID' in request.session:
        doctor_id = request.session['Doctor_ID']

        # Fetching saved patients for the logged-in doctor
        saved_patients = save_doctor.objects.filter(Doctor_ID=doctor_id).values_list('Patient_ID', flat=True)
        
        # Fetch complete patient objects
        patients = Patient.objects.filter(pk__in=saved_patients)

        # Fetching heart disease data for the specific HD_ID associated with the doctor
        ddiabetes_disease_data = Diabetes_Patient.objects.filter(Patient_ID__in=saved_patients, Dia_ID=dia_id).select_related('Dia_ID', 'Patient_ID').first()

        return render(request, 'Doctor/Dia_Detailed.html', {
            'ddiabetes_disease_data': ddiabetes_disease_data,
            'patients': patients
        })
    else:
        return HttpResponseBadRequest('Doctor ID not found in session.')

def Pparkinsons_detail(request, par_id):
    if 'Doctor_ID' in request.session:
        doctor_id = request.session['Doctor_ID']

        # Fetching saved patients for the logged-in doctor
        saved_patients = save_doctor.objects.filter(Doctor_ID=doctor_id).values_list('Patient_ID', flat=True)
        
        # Fetch complete patient objects
        patients = Patient.objects.filter(pk__in=saved_patients)

        # Fetching heart disease data for the specific HD_ID associated with the doctor
        Pparkinsons_disease_data = Parkinsons_Patient.objects.filter(Patient_ID__in=saved_patients, Par_ID=par_id).select_related('Par_ID', 'Patient_ID').first()

        return render(request, 'Doctor/Par_Detailed.html', {
            'Pparkinsons_disease_data': Pparkinsons_disease_data,
            'patients': patients
        })
    else:
        return HttpResponseBadRequest('Doctor ID not found in session.')

def Forgot_P(request):
    return render(request, 'Doctor/forgot_password.html')

def pforgot_password(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the name exists in the database
        if Doctor.objects.filter(Doctor_Name=name).exists():
            # Check if the password and confirm password match
            if password == confirm_password:
                # Update the password in the database
                doctor = Doctor.objects.get(Doctor_Name=name)
                doctor.Doctor_Password = password
                doctor.save()
                messages.success(request, 'Password has been changed')
                # Redirect to a success page or login page
                return redirect('dlogin')  # Redirect to login page
            else:
                # Password and confirm password don't match, show error message
                messages.error(request, 'Passwords do not match.')
        else:
            # Name does not exist, show error message
            messages.error(request, 'Invalid name. Please enter a valid name.')

    return render(request, 'Doctor/forgot_password.html')