from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _ 
from django.core.exceptions import ValidationError

from PIL import Image 

class CustomerManager(BaseUserManager):
    def create_user(self, email, password=None, **otherfields):
        if not email:
            raise ValueError('Users must have email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **otherfields)
        user.set_password(password)
        user.save()
        return user 
    
    def create_superuser(self, email, password=None, **otherfields):
        otherfields.setdefault('is_staff', True)
        otherfields.setdefault('is_active', True)
        otherfields.setdefault('is_superuser', True)

        if otherfields.get('is_staff') is not True:
            raise ValueError('is_staff must be set to True')
        if otherfields.get('is_superuser') is not True:
            raise ValueError('is_super user must be set to True')
        
        return self.create_user(email, password, **otherfields)
    

class MyUser(AbstractUser):
        email = models.EmailField(_('email address'), unique=True)

        objects = CustomerManager()

        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = []

        def __str__(self):
             return self.email 
        

def validate_image_size(image):
    # maximum allowed image size
    max_size = 2 * 1024 * 1024 # 2MB

    if image.size > max_size:
        raise ValidationError("Max image size is 2 MB")
                    

class Profile(models.Model):    
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    avatar = models.ImageField(default='images/default.jpg', upload_to='profile_pics', validators=[validate_image_size])
    bio = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

    def __str__(self):
        return  f'{self.user.username} Profile'       
             
        

