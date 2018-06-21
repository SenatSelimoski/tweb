from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):

    def _create_user(self, username, email, password=None, is_superuser=False, is_active=False):
        if not username:
            raise ValueError(_('Users must have an username provided'))

        if not email:
            raise ValueError(_('Users must have an email provided'))

        if not password:
            raise ValueError(_('Users must have a password provided'))

        user = self.model(
            username = username,
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.is_superuser = is_superuser
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password):
        user = self._create_user(
            username,
            email,
            password = password
            )
        user.is_superuser = False
        user.is_active = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password):
        user = self._create_user(
            username,
            email,
            password = password
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user

