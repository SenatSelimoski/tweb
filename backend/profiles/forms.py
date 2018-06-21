from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import User



class UserCreateForm(UserCreationForm):

    email = forms.EmailField(max_length=150, required=True, help_text=_("Ве молиме внесете е-маил адреса"))
    
    class Meta:
        model = User
        fields = ( 'username' , 'email', 'password1', 'password2',)

class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("This account is inactive.Please check your email for confirmation."),
                code='inactive',
            )
