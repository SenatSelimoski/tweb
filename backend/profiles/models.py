from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from PIL import Image
from io import BytesIO
import os


from .managers import UserManager
class User(AbstractUser):
    username = models.CharField(_('username'),
                                max_length=125,
                                unique=True, 
                                blank=False, 
                                null=False)
    email = models.EmailField(_('email address'),
                                max_length=125,
                                unique=True,
                                blank=False,
                                null=False)
    date_joined  = models.DateTimeField(_('date joined'), auto_now_add=True,editable=False)
    is_active    = models.BooleanField(_('is active'),default=True)
    is_staff     = models.BooleanField(_('is staff'),default=False)
    is_superuser = models.BooleanField(_('is admin'),default=False)
    e_confirmed  = models.BooleanField(_('is email confirmed'),default=False)    



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    def has_perms(self, perm, obj=None ):
        return True
    
    def has_module_perms(self, app_label):
        return True

class Img(models.Model):
    image      = models.ImageField(upload_to='',default=settings.DEFAULT_AVATAR)
    img_web    = models.ImageField(upload_to='web',editable=False, blank=True)
    img_large  = models.ImageField(upload_to='large',editable=False, blank=True)
    img_thumb  = models.ImageField(upload_to='thumb',default='/media/thumb/user-profile_image_thumb.jpg',editable=False, blank=True)

    def save(self, *args, **kwargs):
        t_name, t_ext = os.path.splitext(self.image.name)
        t_ext = t_ext.lower()
        if t_ext in ['.jpeg','.jpg']:
            FTYPE = 'JPEG'
        elif t_ext == '.png':
            FTYPE = 'PNG'
        elif t_ext == '.gif':
            FTYPE = 'GIF'
        else:
            return False

        
        IMAGE_SIZES = {
            'image_web':(300,348),
            'image_large':(600,450),
            'image_thumb':(200,200)
        }
        for f_name, size in IMAGE_SIZES.items():
            
            if f_name == 'image_web':
                img = Image.open(self.image)
                if img.mode not in ('L', 'RGB'):
                    img.convert('RGB')
                img.thumbnail(size, Image.ANTIALIAS)
                iw = f'{t_name}_image_web{t_ext}'
                t_image = BytesIO()
                img.save(t_image, FTYPE)
                t_image.seek(0)

                self.img_web.save(iw, ContentFile(t_image.read()),save=False)
                t_image.close()
                continue

            if f_name == 'image_large':
                img = Image.open(self.image)
                if img.mode not in ('L', 'RGB'):
                    img.convert('RGB')
                iw = f'{t_name}_image_large{t_ext}'
                img.thumbnail(size, Image.ANTIALIAS)
                t_image = BytesIO()
                img.save(t_image, FTYPE)
                t_image.seek(0)

                self.img_large.save(iw, ContentFile(t_image.read()),save=False)
                t_image.close()
                continue

            if f_name == 'image_thumb':
                img = Image.open(self.image)
                if img.mode not in ('L', 'RGB'):
                    img.convert('RGB')
                iw = f'{t_name}_image_thumb{t_ext}'
                img.thumbnail(size, Image.ANTIALIAS)
                t_image = BytesIO()
                img.save(t_image, FTYPE)
                t_image.seek(0)
                self.img_thumb.save(iw, ContentFile(t_image.read()),save=False)
                t_image.close()
                break
        super(Img, self).save(*args, **kwargs)
        storage.delete(self.image)
        
    def __str__(self):
        return self.image.name


class Profile(models.Model):

    user        = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #slug        = models.SlugField(_('slug field'),unique=True)
    first_name  = models.CharField(_('first name'),max_length=150,blank=True,null=True)
    last_name   = models.CharField(_('second name'),max_length=150,blank=True,null=True)
    avatar      = models.ForeignKey(Img,blank=True,null=True,on_delete=models.CASCADE) 
    location    = models.CharField(_('location'),max_length=150,blank=True,null=True)
    contact     = models.CharField(_('contact number'),max_length=150,blank=True)
    certified   = models.BooleanField(_('certified'),default=False)


    def __str__(self):
        return self.user.username

    def get_avatar(self):
        if not self.avatar:
            self.avatar = Img()
        return self.avatar.img_thumb


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
    instance.profile.save()


