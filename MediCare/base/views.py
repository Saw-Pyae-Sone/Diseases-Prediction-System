from django.shortcuts import render, redirect
from .models import Room
from django.http import HttpResponse
from .ml_models.model_loader import load_heart_model, load_diabetes_model, load_parkinsons_model

# Create your views here.

# rooms = [
#     {'id':1, 'name':'lets learn Python'},
#     {'id':2, 'name':'Design with me'},
#     {'id':3, 'name':'Frontend developers'},
# ]

def predict_heart(request):
    heart_diagnosis = ''

    if request.method == 'POST':
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

        if heart_prediction[0] == 1:
            heart_diagnosis = 'The person has Heart Disease'
        else:
            heart_diagnosis = 'The person does not have Heart Disease'

    return render(request, 'MediCare/home.html', {'heart_diagnosis': heart_diagnosis})

def calculate_bmi(weight, height):

    height_in_meters = height/100

    BMI = weight / (height_in_meters ** 2)
    
    return BMI

def predict_diabetes(request):
    diabetes_diagnosis = ''

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

            if diabetes_prediction[0] == 0:
                diabetes_diagnosis = 'The person does not have diabetes'

            elif diabetes_prediction[0] == 1:
                diabetes_diagnosis = 'The person has prediabetes'

            else:
                diabetes_diagnosis = 'The person has diabetes'

        except ValueError:
            diabetes_diagnosis = 'Invalid input values. Please enter valid numbers.'

    return render(request, 'MediCare/Diabetes.html', {'diabetes_diagnosis': diabetes_diagnosis})

def predict_parkinsons(request):
    parkinsons_diagnosis = ''

    if request.method == 'POST':
        Fo = float(request.POST.get('Fo'))
        Fhi = float(request.POST.get('Fhi'))
        Flo = float(request.POST.get('Flo'))
        Jitter_Precentage = float(request.POST.get('Jitter-Precentage'))
        Jitter_Abs = float(request.POST.get('Jitter-Abs'))
        RAP = float(request.POST.get('RAP'))
        PPQ = float(request.POST.get('PPQ'))
        DDP = float(request.POST.get('DDP'))
        Shimmer = float(request.POST.get('Shimmer'))
        Shimmer_Decibles = float(request.POST.get('Shimmer_Decibles'))
        APQ3 = float(request.POST.get('APQ3'))
        APQ5 = float(request.POST.get('APQ5'))
        APQ = float(request.POST.get('APQ'))
        DDA = float(request.POST.get('DDA'))
        NHR = float(request.POST.get('NHR'))
        HNR = float(request.POST.get('HNR'))
        RPDE = float(request.POST.get('RPDE'))
        DFA = float(request.POST.get('DFA'))
        Spread_1 = float(request.POST.get('Spread-1'))
        Spread_2 = float(request.POST.get('Spread-2'))
        D2 = float(request.POST.get('D2'))
        PPE = float(request.POST.get('PPE'))

        # Load the model
        parkinsons_model = load_parkinsons_model()

        # Make a prediction using the ML model
        user_input = [Fo, Fhi, Flo, Jitter_Precentage, Jitter_Abs,
                      RAP, PPQ, DDP, Shimmer, Shimmer_Decibles, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, Spread_1, Spread_2, D2, PPE]

        parkinsons_prediction = parkinsons_model.predict([user_input])

        if parkinsons_prediction[0] == 1:
            parkinsons_diagnosis = 'The person has Parkinsons Disease'
        else:
            parkinsons_diagnosis = 'The person does not have Parkinsons Disease'

    return render(request, 'MediCare/Parkinsons.html', {'parkinsons_diagnosis': parkinsons_diagnosis})

def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'MediCare/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'MediCare/room.html', context)

def createRoom(request):
    context = {}
    return render(request, 'MediCare/room_form.html', context)

def aboutus(request):
    context={}
    return render(request, 'MediCare/AboutUs.html', context)

def diabetes(request):
    context = {}
    return render(request, 'MediCare/Diabetes.html', context)

def parkinsons(request):
    context = {}
    return render(request, 'MediCare/Parkinsons.html', context)

def feedback(request):
    context = {}
    return render(request, 'MediCare/Feedback.html', context)