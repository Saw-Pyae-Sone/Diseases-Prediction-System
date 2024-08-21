from django.shortcuts import render, redirect
from .ml_models.model_loader import load_heart_model, load_diabetes_model, load_parkinsons_model
from .models import Doctor
from django.contrib import messages
from .forms import PatientForm, FeedbackForm, PatientEditForm
from .models import Patient, Heart_Disease, Feedback, Heart_Patient, Diabetes_Patient, save_doctor, Diabetes, Parkinsons_Patient, Parkinsons, Medical_Preventation
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from base.backend import PatientBackend
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.db.models import Q

def predict_heart(request):
    heart_diagnosis = ''
    heart_condition = -1

    if request.method == 'POST':
        try:
            age = float(request.POST.get('age'))
            sex = float(request.POST.get('sex'))
            cp = float(request.POST.get('cp'))
            trestbps = float(request.POST.get('trestbps'))
            chol = float(request.POST.get('chol'))
            fbs = float(request.POST.get('fbs'))
            restecg = float(request.POST.get('restecg'))
            thalach = float(request.POST.get('thalach'))
            exang = float(request.POST.get('exang'))
            oldpeak = float(request.POST.get('oldpeak'))
            slope = float(request.POST.get('slope'))
            ca = float(request.POST.get('ca'))
            thal = float(request.POST.get('thal'))

            # Load the model
            heart_model = load_heart_model()

            # Make a prediction using the ML model
            user_input = [age, sex, cp, trestbps, chol,
                        fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]

            heart_prediction = heart_model.predict([user_input])

            # If 'Patient_ID' is not in the session, return a bad request response
            if 'Patient_ID' not in request.session:
                return HttpResponseBadRequest('Patient_ID not found in session.')

            # Get the patient ID from the session
            patient_id = request.session.get('Patient_ID')

            # Get the patient instance based on the patient_id
            patient_instance = Patient.objects.get(Patient_ID=patient_id)

            # Create a Heart_Disease instance
            heart_disease_instance = Heart_Disease.objects.create(
                age=age,
                sex=sex,
                cp=cp,
                trestbps=trestbps,
                chol=chol,
                fbs=fbs,
                restecg=restecg,
                thalach=thalach,
                exang=exang,
                oldpeak=oldpeak,
                slope=slope,
                ca=ca,
                thal=thal,
                target=heart_prediction[0]
            )

            # Make a prediction using the ML model
            heart_prediction_prob = heart_model.predict_proba([user_input])

            # Get the probability of class 1 (having heart disease)
            probability_of_disease = heart_prediction_prob[0][1]  # Assuming class 1 is the second class

            # Calculate positive and negative percentages
            positive_percentage = round(probability_of_disease * 100)
            negative_percentage = 100 - positive_percentage

            # Determine the diagnosis message based on the prediction and probability
            if heart_prediction[0] == 1:
                heart_diagnosis = f'The person has Heart Disease with {positive_percentage}% confidence'
                heart_condition = 1
            else:
                heart_diagnosis = f'The person does not have Heart Disease with {negative_percentage}% confidence'
                heart_condition = 0

            # Create a Heart_Patient instance
            heart_patient_instance = Heart_Patient.objects.create(
                HD_ID=heart_disease_instance,
                Patient_ID=patient_instance,
                Heart_Percentages=positive_percentage
            )

            disease_doctors = Doctor.objects.filter(Doctor_Specialty='Heart_diseases')
            medical_pre = Medical_Preventation.objects.filter(Diseases = 'Heart_diseases')

            return render(request, 'MediCare/home.html', 
            {
                'heart_diagnosis': heart_diagnosis, 
                'heart_condition': heart_condition,
                'disease_doctors': disease_doctors, 
                'medical_pre': medical_pre,
            })

        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'MediCare/home.html')

    # Handle GET requests by rendering a form for user input
    return render(request, 'MediCare/home.html')

def calculate_bmi(weight, height):

    height_in_meters = height/100

    BMI = weight / (height_in_meters ** 2)
    
    return BMI

def predict_diabetes(request):
    diabetes_diagnosis = ''
    diabetes_condition = -1 

    if request.method == 'POST':
        try:
            # Check and convert form values
            HighBP = int(request.POST.get('HighBP'))
            HighChol = int(request.POST.get('HighChol', 0))
            CholCheck = int(request.POST.get('CholCheck'))
            weight = float(request.POST.get('Weight', 0))
            height = float(request.POST.get('Height', 0))
            BMI = calculate_bmi(weight, height)
            Smoker = int(request.POST.get('Smoker', 0))
            Stroke = int(request.POST.get('Stroke', 0))
            HeartDiseaseorAttack = int(request.POST.get('HeartDiseaseorAttack', 0))
            PhysActivity = int(request.POST.get('PhysActivity'))
            Fruits = int(request.POST.get('Fruits'))
            Veggies = int(request.POST.get('Veggies'))
            HvyAlcoholConsump = int(request.POST.get('HvyAlcoholConsump'))
            AnyHealthcare = int(request.POST.get('AnyHealthcare'))
            NoDocbcCost = int(request.POST.get('NoDocbcCost', 0))
            GenHlth = int(request.POST.get('GenHlth', 0))
            MentHlth = int(request.POST.get('MentHlth', 0))
            PhysHlth = int(request.POST.get('PhysHlth', 0))
            DiffWalk = int(request.POST.get('DiffWalk', 0))
            Sex = int(request.POST.get('Sex'))
            Age = int(request.POST.get('Age'))
            Education = int(request.POST.get('Education', 0))
            Income = float(request.POST.get('Income', 0))

            # Load the model
            diabetes_model = load_diabetes_model()

            # Make a prediction using the ML model
            user_input = [HighBP, HighChol, CholCheck, BMI, Smoker, Stroke, HeartDiseaseorAttack, PhysActivity, Fruits,
                          Veggies, HvyAlcoholConsump, AnyHealthcare, NoDocbcCost, GenHlth, MentHlth, PhysHlth, DiffWalk,
                          Sex, Age, Education, Income]

            diabetes_prediction = diabetes_model.predict([user_input])
            diabetes_prediction_prob = diabetes_model.predict_proba([user_input])

            probability_of_diabetes = diabetes_prediction_prob[0][1]

            # Determine the diagnosis message based on the prediction and probability
            if diabetes_prediction[0] == 1:
                diabetes_diagnosis = f'The person has prediabetes with {probability_of_diabetes * 100:.2f}% confidence'
                diabetes_condition = 1
            elif diabetes_prediction[0] == 2:
                diabetes_diagnosis = f'The person has diabetes with {probability_of_diabetes * 100:.2f}% confidence'
                diabetes_condition = 2
            else:
                diabetes_diagnosis = f'The person does not have diabetes'
                diabetes_condition = 0

            # If 'Patient_ID' is not in the session, return a bad request response
            if 'Patient_ID' not in request.session:
                return HttpResponseBadRequest('Patient_ID not found in session.')

            # Get the patient ID from the session
            patient_id = request.session.get('Patient_ID')

            # Get the patient instance based on the patient_id
            patient_instance = Patient.objects.get(Patient_ID=patient_id)

            # Create a Diabetes instance
            diabetes_instance = Diabetes.objects.create(
                Diabetes_012 = diabetes_prediction[0],
                HighBP=HighBP,
                HighChol=HighChol,
                CholCheck=CholCheck,
                BMI=BMI,
                Smoker=Smoker,
                Stroke=Stroke,
                HeartDiseaseorAttack=HeartDiseaseorAttack,
                PhysActivity=PhysActivity,
                Fruits=Fruits,
                Veggies=Veggies,
                HvyAlcoholConsump=HvyAlcoholConsump,
                AnyHealthcare=AnyHealthcare,
                NoDocbcCost=NoDocbcCost,
                GenHlth=GenHlth,
                MentHlth=MentHlth,
                PhysHlth=PhysHlth,
                DiffWalk=DiffWalk,
                Sex=Sex,
                Age=Age,
                Education=Education,
                Income=Income
            )

            # Create a Diabetes_Patient instance
            diabetes_patient_instance = Diabetes_Patient.objects.create(
                Dia_ID=diabetes_instance,
                Patient_ID=patient_instance,
                Diabetes_Percentages=probability_of_diabetes * 100
            )

        except ValueError:
            diabetes_diagnosis = 'Invalid input values. Please enter valid numbers.'

    disease_doctors = Doctor.objects.filter(Doctor_Specialty='Diabetes')
    medical_pre = Medical_Preventation.objects.filter(Diseases = 'Diabetes')
    return render(request, 'MediCare/Diabetes.html', {
        'diabetes_diagnosis': diabetes_diagnosis,
        'diabetes_condition': diabetes_condition,
        'disease_doctors': disease_doctors,
        'medical_pre': medical_pre,
    })

def predict_parkinsons(request):
    parkinsons_diagnosis = ''
    parkinsons_condition = -1  # Default value to indicate no prediction

    if request.method == 'POST':
        try:
            # Extract and convert form values, providing default values if necessary
            Fo = float(request.POST.get('MDVP:Fo(Hz)', 'nan'))
            Fhi = float(request.POST.get('MDVP:Fhi(Hz)', 'nan'))
            Flo = float(request.POST.get('MDVP:Flo(Hz)', 'nan'))
            Jitter_Percentage = float(request.POST.get('MDVP:Jitter(%)', 'nan'))
            Jitter_Abs = float(request.POST.get('MDVP:Jitter(Abs)', 'nan'))
            RAP = float(request.POST.get('MDVP:RAP', 'nan'))
            PPQ = float(request.POST.get('MDVP:PPQ', 'nan'))
            DDP = float(request.POST.get('Jitter:DDP', 'nan'))
            Shimmer = float(request.POST.get('MDVP:Shimmer', 'nan'))
            Shimmer_Decibles = float(request.POST.get('MDVP:Shimmer(dB)', 'nan'))
            APQ3 = float(request.POST.get('Shimmer:APQ3', 'nan'))
            APQ5 = float(request.POST.get('Shimmer:APQ5', 'nan'))
            APQ = float(request.POST.get('MDVP:APQ', 'nan'))
            DDA = float(request.POST.get('Shimmer:DDA', 'nan'))
            NHR = float(request.POST.get('NHR', 'nan'))
            HNR = float(request.POST.get('HNR', 'nan'))
            RPDE = float(request.POST.get('RPDE', 'nan'))
            DFA = float(request.POST.get('DFA', 'nan'))
            Spread_1 = float(request.POST.get('spread1', 'nan'))
            Spread_2 = float(request.POST.get('spread2', 'nan'))
            D2 = float(request.POST.get('D2', 'nan'))
            PPE = float(request.POST.get('PPE', 'nan'))

            # Check for any 'nan' values and handle them accordingly
            if any([value != value for value in [Fo, Fhi, Flo, Jitter_Percentage, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_Decibles, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, Spread_1, Spread_2, D2, PPE]]):
                raise ValueError('Missing or invalid input values.')

            # Load the model
            parkinsons_model = load_parkinsons_model()

            # Make a prediction using the ML model
            user_input = [Fo, Fhi, Flo, Jitter_Percentage, Jitter_Abs,
                          RAP, PPQ, DDP, Shimmer, Shimmer_Decibles, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, Spread_1, Spread_2, D2, PPE]

            parkinsons_prediction = parkinsons_model.predict([user_input])
            parkinsons_prediction_prob = parkinsons_model.predict_proba([user_input])

            probability_of_parkinsons = parkinsons_prediction_prob[0][1]

            # Determine the diagnosis message based on the prediction and probability
            if parkinsons_prediction[0] == 1:
                parkinsons_diagnosis = f'The person has Parkinson\'s Disease with {probability_of_parkinsons * 100:.2f}% confidence'
                parkinsons_condition = 1
            else:
                parkinsons_diagnosis = f'The person does not have Parkinson\'s Disease with {(1 - probability_of_parkinsons) * 100:.2f}% confidence'
                parkinsons_condition = 0

            # If 'Patient_ID' is not in the session, return a bad request response
            if 'Patient_ID' not in request.session:
                return HttpResponseBadRequest('Patient_ID not found in session.')

            # Get the patient ID from the session
            patient_id = request.session.get('Patient_ID')

            # Get the patient instance based on the patient_id
            patient_instance = Patient.objects.get(Patient_ID=patient_id)

            # Create a Parkinsons instance
            parkinsons_instance = Parkinsons.objects.create(
                MDVP_FO_Hz=Fo,
                MDVP_Fhi_Hz=Fhi,
                MDVP_Flo_hz=Flo,
                MDVP_Jitter_percentage=Jitter_Percentage,
                MDVP_Jibber_Abs=Jitter_Abs,
                MDVP_RAP=RAP,
                MDVP_PPQ=PPQ,
                Jitter_DDP=DDP,
                MDVP_Shimmer=Shimmer,
                MDVP_Shimmer_dB=Shimmer_Decibles,
                Shimmer_APQ3=APQ3,
                Shimmer_APQ5=APQ5,
                MDVP_APQ=APQ,
                Shimmer_DDA=DDA,
                NHR=NHR,
                HNR=HNR,
                RPDE=RPDE,
                DFA=DFA,
                spread1=Spread_1,
                spread2=Spread_2,
                D2=D2,
                PPE=PPE,
                status=parkinsons_prediction[0]
            )

            # Create a Parkinsons_Patient instance
            parkinsons_patient_instance = Parkinsons_Patient.objects.create(
                Par_ID=parkinsons_instance,
                Patient_ID=patient_instance,
                Parkinsons_Percentages=probability_of_parkinsons * 100
            )

        except ValueError as e:
            print(f'Fo value: {Fo}')
            print(f'Error: {e}')
            print(f'Form values: {request.POST}')
            parkinsons_diagnosis = 'Invalid input values. Please enter valid numbers.'
            print(f'Error: {e}')

    disease_doctors = Doctor.objects.filter(Doctor_Specialty='Parkinsons')
    medical_pre = Medical_Preventation.objects.filter(Diseases = 'Parkinsons')
    return render(request, 'MediCare/Parkinsons.html', {
        'parkinsons_diagnosis': parkinsons_diagnosis,
        'parkinsons_condition': parkinsons_condition,
        'disease_doctors': disease_doctors,
        'medical_pre': medical_pre,
    })

def home(request):
    context = {}
    return render(request, 'MediCare/home.html', context)

def aboutus(request):
    doctors = Doctor.objects.all()
    context = {'doctors': doctors}
    return render(request, 'MediCare/about.html', context)

def diabetes(request):
    context = {}
    return render(request, 'MediCare/Diabetes.html', context)

def parkinsons(request):
    context = {}
    return render(request, 'MediCare/Parkinsons.html', context)

def feedback(request):
    if 'Patient_ID' in request.session:
        context = {}
        return render(request, 'MediCare/Feedback.html', context)
    else:
        return redirect('plogin')

def index(request):
    patientdata = Patient.objects.all()
    doctors = Doctor.objects.all()
    context = {'patient': patientdata, 'doctors': doctors}
    return render(request, 'MediCare/index.html', context)

def login(request):
    context = {}
    return render(request, 'MediCare/Login.html', context)

def doctor(request):
    doctors = Doctor.objects.all()
    context = {'doctors': doctors}
    return render(request, 'MediCare/doctors.html', context)

def register(request):
    context = {}
    return render(request, 'MediCare/Register.html', context)

def register_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient registered successfully.')
            return redirect('register')
        else:
            # Print form errors to the console or log them
            print(form.errors)
            messages.error(request, 'Form is not valid. Please check the input data.')
    else:
        form = PatientForm()
    return render(request, 'MediCare/Register.html', {'form': form})

def custom_Plogin(request):
     
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = PatientBackend().authenticate(request, email=email, password=password)

            if user is not None and hasattr(user, 'Patient_ID'):
                request.session['Patient_ID'] = user.Patient_ID
                messages.success(request, f'Welcome, {email}!')
                print("Patient ID:", request.session.get('Patient_ID'))
                return redirect('index')
            else:
                messages.error(request, 'Invalid email or password.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    return render(request, 'MediCare/Login.html')

def custom_plogout(request):
    if 'Patient_ID' in request.session:
        del request.session['Patient_ID']
    request.session.flush() 
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('index')

def History(request):
    if 'Patient_ID' in request.session:
        patient_id = request.session['Patient_ID']

        # Fetch heart disease data for the logged-in patient
        heart_disease_data = Heart_Patient.objects.filter(Patient_ID=patient_id).select_related('HD_ID', 'Patient_ID')

        # Fetch diabetes data for the logged-in patient
        diabetes_data = Diabetes_Patient.objects.filter(Patient_ID=patient_id).select_related('Dia_ID', 'Patient_ID')
        
        # Fetch parkinsons data for the logged-in patient
        parkinsons_data = Parkinsons_Patient.objects.filter(Patient_ID=patient_id).select_related('Par_ID', 'Patient_ID')

        context = {
            'heart_disease_data': heart_disease_data,
            'diabetes_data': diabetes_data,
            'parkinsons_data': parkinsons_data
        }

        return render(request, 'MediCare/History.html', context)
    else:
        return HttpResponseBadRequest('Patient ID not found in session.')

def heart_detail(request, hd_id):
    if 'Patient_ID' in request.session:
        patient_id = request.session['Patient_ID']

        # Fetch heart disease data for the logged-in patient
        heart_disease_data = Heart_Patient.objects.filter(Patient_ID=patient_id, HD_ID=hd_id).select_related('HD_ID', 'Patient_ID')
        print(f'Heart disease data: {heart_disease_data}')  # Debug print
        
        # Fetch saved doctors for the logged-in patient
        saved_doctors = save_doctor.objects.filter(Patient_ID=patient_id).select_related('Doctor_ID')
        print(f'Saved doctors: {saved_doctors}')  # Debug print

        return render(request, 'MediCare/Heart_Detailed.html', {
            'heart_disease_data': heart_disease_data,
            'saved_doctors': saved_doctors
        })
    else:
        return HttpResponseBadRequest('Patient ID not found in session.')
    
def diabetes_detail(request, dd_id):
    if 'Patient_ID' in request.session:
        patient_id = request.session['Patient_ID']

        # Fetch diabetes data for the logged-in patient
        diabetes_data = Diabetes_Patient.objects.filter(Patient_ID=patient_id, Diabetes_Patient_ID=dd_id).select_related('Dia_ID', 'Patient_ID')
        print(f'Diabetes data: {diabetes_data}')  # Debug print
        
        # Fetch saved doctors for the logged-in patient
        saved_doctors = save_doctor.objects.filter(Patient_ID=patient_id).select_related('Doctor_ID')
        print(f'Saved doctors: {saved_doctors}')  # Debug print

        return render(request, 'MediCare/Dia_Detailed.html', {
            'diabetes_data': diabetes_data,
            'saved_doctors': saved_doctors
        })
    else:
        return HttpResponseBadRequest('Patient ID not found in session.')

def parkinsons_detail(request, par_id):
    if 'Patient_ID' in request.session:
        patient_id = request.session['Patient_ID']

        # Fetch Parkinsons data for the logged-in patient
        parkinsons_data = Parkinsons_Patient.objects.filter(Patient_ID=patient_id, Par_ID=par_id).select_related('Par_ID', 'Patient_ID')
        print(f'Parkinsons data: {parkinsons_data}')  # Debug print
        
        # Fetch saved doctors for the logged-in patient
        saved_doctors = save_doctor.objects.filter(Patient_ID=patient_id).select_related('Doctor_ID')
        print(f'Saved doctors: {saved_doctors}')  # Debug print

        return render(request, 'MediCare/Par_Detailed.html', {
            'parkinsons_data': parkinsons_data,
            'saved_doctors': saved_doctors
        })
    else:
        return HttpResponseBadRequest('Patient ID not found in session.')
    
def profile(request):
    if 'Patient_ID' in request.session:
        patient_id = request.session['Patient_ID']
        try:
            patient = Patient.objects.get(pk=patient_id)
            profile_picture_name = patient.Patient_Image.url if patient.Patient_Image else None
            patient_family_medical_history = patient.Patient_Family_Medical_History.url if patient.Patient_Family_Medical_History else None
            context = {
                'patient': patient,
                'profile_picture_name': profile_picture_name,
                'patient_family_medical_history': patient_family_medical_history,
            }
        except Patient.DoesNotExist:
            messages.error(request, 'Patient does not exist.')
            context = {}
    else:
        messages.error(request, 'You need to log in to view this page.')
        context = {}

    return render(request, 'MediCare/Profile.html', context)


def edit_patient(request):
    if 'Patient_ID' in request.session:
        patient_id = request.session['Patient_ID']
        try:
            patient = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            return redirect('profile')

        if request.method == 'POST':
            form = PatientEditForm(request.POST, request.FILES, instance=patient)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('profile')
            else:
                messages.error(request, 'Form is not valid. Please check the input data.')
                return render(request, 'MediCare/Profile.html', {'form': form, 'patient': patient})
        else:
            form = PatientForm(instance=patient)

        return render(request, 'MediCare/Profile.html', {'form': form, 'patient': patient})
    else:
        return redirect('profile')
    
def feedback_add(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            
            if 'Patient_ID' in request.session:
                patient_id = request.session['Patient_ID']
                try:
                    patient = Patient.objects.get(pk=patient_id)
                    feedback.Patient_ID = patient
                except Patient.DoesNotExist:
                    messages.error(request, 'Patient not found.')
                    return redirect('plogin')
            else:
                messages.error(request, 'Patient ID not found in session.')
                return redirect('plogin')

            feedback.save()

            messages.success(request, 'Feedback submitted successfully.')

            return redirect('feedback')
        else:
            messages.error(request, 'Form is not valid. Please check the input data.')
            return render(request, 'MediCare/Feedback.html', {'form': form})
    else:
        form = FeedbackForm()
    return render(request, 'MediCare/Feedback.html', {'form': form})

def sdoctor(request, doctor_id):
    try:
        doctor = Doctor.objects.get(pk=doctor_id)
    except Doctor.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Doctor Not Found'}, status=404)

    if request.method == 'POST':
        patient_id = request.session.get('Patient_ID')
        if not patient_id:
            return JsonResponse({'success': False, 'message': 'Please log in to save the doctor.'}, status=401)

        try:
            patient = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Patient Not Found'}, status=404)
        
        # Check if the doctor is already saved by the patient
        if save_doctor.objects.filter(Q(Patient_ID=patient) & Q(Doctor_ID=doctor)).exists():
            return JsonResponse({'success': False, 'message': 'Doctor already saved by the patient'})

        # If not, create a new saved doctor record
        new_saved_doctor = save_doctor.objects.create(Patient_ID=patient, Doctor_ID=doctor)
        if new_saved_doctor:
            return JsonResponse({'success': True, 'message': 'Successfully Saved'})
        else:
            return JsonResponse({'success': False, 'message': 'Failed to save the doctor'})

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)

def remove_doctor(request, doctor_id):
    if request.method == 'POST':
        patient_id = request.session.get('Patient_ID')
        if not patient_id:
            return JsonResponse({'success': False, 'message': 'Please log in to remove the doctor.'}, status=401)
        
        try:
            patient = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Patient Not Found'}, status=404)

        try:
            saved_doctor = save_doctor.objects.get(Patient_ID=patient, Doctor_ID=doctor_id)
            saved_doctor.delete()
            return JsonResponse({'success': True, 'message': 'Successfully Removed'})
        except save_doctor.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Doctor Not Found in Saved List'}, status=404)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)

def Forgot_P(request):
    return render(request, 'MediCare/Forgot_password.html')

def mforgot_password(request):
    if request.method == 'POST':
        name = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the name exists in the database
        if Patient.objects.filter(Patient_Email=name).exists():
            # Check if the password and confirm password match
            if password == confirm_password:
                # Update the password in the database
                patient = Patient.objects.get(Patient_Email=name)
                patient.Patient_Password = password
                patient.save()
                messages.success(request, 'Password has been changed')
                # Redirect to a success page or login page
                return redirect('plogin')  # Redirect to login page
            else:
                # Password and confirm password don't match, show error message
                messages.error(request, 'Passwords do not match.')
        else:
            # Name does not exist, show error message
            messages.error(request, 'Invalid email. Please enter a valid email.')

    return render(request, 'MediCare/Forgot_password.html')


def mel_prevention(request):
    heart_medical = Medical_Preventation.objects.filter(Diseases = 'Heart_diseases')
    diabetes_medical = Medical_Preventation.objects.filter(Diseases = 'Diabetes')
    parkinsons_medical = Medical_Preventation.objects.filter(Diseases = 'Parkinsons')

    context={
        'heart_medical': heart_medical,
        'diabetes_medical': diabetes_medical,
        'parkinsons_medical': parkinsons_medical,
    }
    return render(request, 'MediCare/Medical_Prevention.html', context)