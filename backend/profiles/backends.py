from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


class UserAuthentication(ModelBackend):

    
    def authenticate(request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            try:
                user = UserModel._default_manager.get_by_natural_key(username)
                if user.check_password(password):
                    return user
            except:
                user = UserModel.objects.get(username=username)
                if user.check_password(password):
                    return user
        except: 
            UserModel.DoesNotExist
        finally:
            try:
                pass
            except:
                UserModel().set_password(password)
                return None
        
    def get_user(self, id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=id)
        except UserModel.DoesNotExist:
            return None
        
