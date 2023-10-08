from rest_framework import serializers
from accounts.models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt import  views as jwt_views, serializers as jwt_serializers, exceptions as jwt_exceptions
from django.contrib import auth 
from django.contrib.auth import login


from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields =['id','mobile_number','email','organization','owner','password']
        extra_kwargs={
            'password':{'write_only':True},

        }
    # def validate(self, attrs):
    #    password = attrs.get('password')
    #    password2=attrs.get('password2')
    #    if password != password2:
    #     raise serializers.ValidationError("Passwords are not matching")
    #    return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField()
    password=serializers.CharField(max_length=68,write_only=True)
    tokens=serializers.CharField(read_only=True)
    class Meta:
        model=User
        fields=['email','password','tokens'] 
    def validate(self,attrs):
        email=attrs.get('email','')
        password=attrs.get('password','')

        user=auth.authenticate(email=email,password=password)
      
        if not user:
            raise AuthenticationFailed('Email or Password is Incorrect!')
        # if not user.isverified:
        #     raise AuthenticationFailed('Email is not Verified!')
        return {
            'mobile_number':user.mobile_number,
            'full_name':user.full_name,
            'email':user.email,
            'tokens':user.tokens
        }



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','mobile_number','email','full_name','age']

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_messages = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self,attrs):
        self.token= attrs['refresh']
        return attrs


    def save(self,**kwargs):
        try:
            RefreshToken(self.token).blacklist()
        
        
        except TokenError:
            self.fail('bad_token')

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email=serializers.EmailField(min_length=2)
    class Meta:
        model=User
        fields=['email'] 
    def validate(self,attrs):
        email=attrs.get('email','')

        user=auth.authenticate(email=email)
        if not user:
            raise AuthenticationFailed('Email is Incorrect!')
        if not user.isverified:
            raise AuthenticationFailed('Email is not Verified!')
        return {
            'email':user.email,
        }
class SetNewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(min_length=6,max_length=68,write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    class Meta :
        fields=['password','token','uidb64']
    def validate(self,attrs):
        try:
            password = attrs.get('password')
            token=attrs.get('token')
            uidb64=attrs.get('uidb64')

            id =force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)
from django.conf import settings
class CookieTokenRefreshSerializer(jwt_serializers.TokenRefreshSerializer):
    refresh = None
    token=serializers.CharField(max_length=555)
    class Meta :
        fields=['token']
    def validate(self, attrs):
        #attrs['refresh'] = self.context['request'].COOKIES.get('refresh')
        # attrs['refresh'] = settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH']
        
        attrs['refresh'] = attrs.get('token')
        
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise jwt_exceptions.InvalidToken(
                'No valid token found in cookie \'refresh\'')

