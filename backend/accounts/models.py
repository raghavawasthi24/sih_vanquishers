from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken



class UserManager(BaseUserManager):
    def create_user(self,email, organization , owner,mobile_number, password=None):
        """
        Creates and saves a User with the given email, name ,tc and password.
        """
        if not mobile_number:
            raise ValueError('Users must have a Mobile Number.')
        if not email:
            raise ValueError('Users must have a Email.')

        user = self.model(
            mobile_number=mobile_number,
            email=self.normalize_email(email),
            organization=organization,
            owner=owner
        )

        user.set_password(password)
        user.isverified=True
        user.save(using=self._db)
        return user

    def create_superuser(self,email, organization , owner,mobile_number,password=None):
        """
        Creates and saves a superuser with the given email, name , tc and password.
        """
        if not mobile_number:
            raise ValueError('Users must have a Mobile number.')
        if not email:
            raise ValueError('Users must have a Email.')
        user = self.create_user(
            mobile_number=mobile_number,
            password=password,
            email=email,
            organization=organization,
            owner=owner
            
        )
        user.is_admin = True
        user.isverified=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    organization=models.CharField(max_length=30)
    owner=models.CharField(max_length=30)
    email=models.EmailField(unique=True)
    mobile_number=models.CharField(max_length=10,unique=True)
    isverified=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at=models.DateField(default=timezone.now)



    objects=UserManager()


    USERNAME_FIELD='email'
    REQUIRED_FIELDS= ['mobile_number','organization','owner']

    def __str__(self):
        return self.organization

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return{
            'refresh': str(refresh),
            'access':str(refresh.access_token)
        }









# Create your models here.
