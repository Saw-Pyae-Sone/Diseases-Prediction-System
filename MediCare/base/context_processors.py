from .models import Patient

def profile_picture(request):
    profile_picture_name = None
    if 'Patient_ID' in request.session:
        patient_id = request.session['Patient_ID']
        try:
            patient = Patient.objects.get(pk=patient_id)
            profile_picture_name = patient.Patient_Image.url
        except Patient.DoesNotExist:
            pass
    return {'profile_picture_name': profile_picture_name}