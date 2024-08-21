from base.models import Admin

def admin_profile_picture(request):
    admin_profile_picture_name = None
    if 'Admin_ID' in request.session:
        admin_id = request.session['Admin_ID']
        try:
            admin = Admin.objects.get(pk=admin_id)
            admin_profile_picture_name = admin.Admin_Image.url
        except Admin.DoesNotExist:
            pass
    return {'admin_profile_picture_name':  admin_profile_picture_name}
