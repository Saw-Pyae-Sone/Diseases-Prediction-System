import pickle
from django.conf import settings
import os

def load_heart_model():
    model_path = os.path.join(settings.BASE_DIR, 'base', 'ml_models', 'heart_model.pkl')
    
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    
    return model

def load_diabetes_model():
    model_path = os.path.join(settings.BASE_DIR, 'base', 'ml_models', 'diabetes_model.pkl')
    
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    
    return model

def load_parkinsons_model():
    model_path = os.path.join(settings.BASE_DIR, 'base', 'ml_models', 'parkinsons_model.pkl')
    
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    
    return model
