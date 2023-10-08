from rest_framework.response import Response
from rest_framework import status, generics ,permissions
from accounts.serializers import *
from accounts.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .models import User
from accounts import serializers,models
import jwt
from django.conf import settings
from drf_yasg import openapi 
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.middleware import csrf
from rest_framework import exceptions as rest_exceptions, response, decorators as rest_decorators, permissions as rest_permissions
from rest_framework_simplejwt import tokens, views as jwt_views, serializers as jwt_serializers, exceptions as jwt_exceptions

from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.generics import RetrieveUpdateDestroyAPIView
import random
import string
b=1
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tokencheck(request):
    return Response({"LoggedIn":"True"})


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)
    # permission_classes=(IsAdminUser,)
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # user_data = serializer.data
        # email_body = 'Hi '+user.full_name + \
            # ' You are registered as faculty at Vanquisher Academy of Education.\nWelcome to our team.'
        # data = {'to_email': user.email,
                # 'email_subject': 'Welcome to our team!','passwd':password}
     

        # Util.send_email(data)
        return Response({"message":"User created successfully"}, status=status.HTTP_201_CREATED)


# class VerifyEmail(APIView):
#     serializer_class = EmailVerificationSerializer

#     token_param_config = openapi.Parameter(
#         'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

#     @swagger_auto_schema(manual_parameters=[token_param_config])
#     def get(self, request):
#         token = request.GET.get('token')
#         try:
#             payload = jwt.decode(token, settings.SECRET_KEY,algorithms=["HS256"])
#             user = User.objects.get(id=payload['user_id'])
#             if not user.isverified:
#                 user.isverified = True
#                 user.save()
#             return redirect("https://team-csi-trainees.github.io/Raghav-Authentication/")
#         except jwt.ExpiredSignatureError as identifier:
#              return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
#         except jwt.exceptions.DecodeError as identifier:
#              return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    serializer_class=LoginSerializer
    def post(self,request):
        data=request.data
        serializer=self.serializer_class(data=request.data)
        email=request.data.get('email','')
        password=request.data.get('password','')  
        user = authenticate(email=email, password=password)
        admin_data={"Admin":user.is_admin}
        if user is not None:
            tokens =user.tokens()
            res = response.Response()
            res.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=tokens["access"],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )

            res.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=tokens["refresh"],
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )

            res["X-CSRFToken"] = csrf.get_token(request)
            res.data = [tokens,admin_data]
            return res
        raise rest_exceptions.AuthenticationFailed("Email or Password is incorrect!")
class CookieTokenRefreshView(jwt_views.TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        refreshToken = request.COOKIES.get(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        token = tokens.RefreshToken(refreshToken)
        if response.data.get("refresh"):
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                value=response.data['refresh'],
                expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )

            del response.data["refresh"]
        response["X-CSRFToken"] = request.COOKIES.get("csrftoken")
        return super().finalize_response(request, response, *args, **kwargs)



class LogoutAPIView(generics.GenericAPIView):
    serializer_class=LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        serializer= self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
@rest_decorators.api_view(['POST'])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def logoutView(request):
    try:
        refreshToken = request.COOKIES.get(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        token = tokens.RefreshToken(refreshToken)
        token.blacklist()

        res = response.Response()
        res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'])
        res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        res.delete_cookie("X-CSRFToken")
        res.delete_cookie("csrftoken")
        res["X-CSRFToken"]=None
        return res
    except:
        raise rest_exceptions.ParseError("Invalid token")
class RequestPasswordRestEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    def post(self,request):

        serializers=self.serializer_class(data=request.data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relative_link = reverse('password-reset',kwargs={'uidb64':uidb64,'token':token})
            absurl = 'http://' + current_site + relative_link
            email_body = 'Hello Use link below to reset your password \n '+"For reset password "+absurl +"\n"+"Your Old Password:"+ user.password2
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reset your Password'}
            Util.send_email(data)
        return Response({'sucess':'We have sent you a link of reset password'},status=status.HTTP_200_OK)
class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    def get(self,request,uidb64,token):
        try:
            id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=id)



            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response({'error':'Token is not valid request for new one'},status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'message': 'creadentials Valid', 'uidb64': uidb64, 'token': token},status=status.HTTP_200_OK)
            #return redirect("https://team-csi-trainees.github.io/Raghav-Authentication/" ,{'success': True, 'message': 'creadentials Valid', 'uidb64': uidb64, 'token': token})
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error':'Token is not  valid'},status=status.HTTP_401_UNAUTHORIZED)

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class=SetNewPasswordSerializer
    def patch(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'sucess':True,'message':'Password reset success'},status=status.HTTP_200_OK)
@rest_decorators.api_view(["GET"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def user(request):
    try:
        user = models.Account.objects.get(id=request.user.id)
    except models.Account.DoesNotExist:
        return response.Response(status_code=404)

    serializer = serializers.AccountSerializer(user)
    return response.Response(serializer.data)





