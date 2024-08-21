from base.models import Doctor

def doctor_profile_picture(request):
    doctor_profile_picture_name = None
    if 'Doctor_ID' in request.session:
        doctor_id = request.session['Doctor_ID']
        try:
            doctor = Doctor.objects.get(pk=doctor_id)
            doctor_profile_picture_name = doctor.Doctor_Image.url
        except Doctor.DoesNotExist:
            pass
    return {'doctor_profile_picture_name': doctor_profile_picture_name}