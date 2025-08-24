from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class ModelBackend(ModelBackend):
    def authenticate(self, request, username_or_email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username_or_email)
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(username=username_or_email)
            except UserModel.DoesNotExist:
                return None
        
        if user.check_password(password):
            return user
                
        return None
    