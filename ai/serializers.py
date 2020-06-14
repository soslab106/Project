from rest_framework import serializers
from .models import File #, FaceRecFile
from django.contrib.auth.models import User
# from google.oauth2 import id_token
# from google.auth.transport import requests

from Project.settings import SOCIAL_GOOGLE_CLIENT_ID
# from models import SocialAccount
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"

# class FaceRecFileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FaceRecFile
#         fields = "__all__"

# class SocialLoginSerializer(serializers.Serializer):
#     token = serializers.CharField(required=True)
#     def verify_token(self, token):
#         """
#         驗證 id_token 是否正確
#         token: JWT
#         """
#         try:
#             idinfo = id_token.verify_oauth2_token(
#                 token, requests.Request(), SOCIAL_GOOGLE_CLIENT_ID)
#             if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
#                 raise ValueError('Wrong issuer.')
#             if idinfo['aud'] not in [SOCIAL_GOOGLE_CLIENT_ID]:
#                 raise ValueError('Could not verify audience.')
#             # Success
#             return idinfo
#         except ValueError:
#             pass
#     def create(self, validated_data):
#         idinfo = self.verify_token(validated_data.get('token'))
#         if idinfo:
#             # User not exists
#             if not SocialAccount.objects.filter(unique_id=idinfo['sub']).exists():
#                 user = User.objects.create_user(
#                     username=f"{idinfo['name']} {idinfo['email']}", # Username has to be unique
#                     first_name=idinfo['given_name'],
#                     last_name=idinfo['family_name'],
#                     email=idinfo['email']
#                 )
#                 SocialAccount.objects.create(
#                     user=user,
#                     unique_id=idinfo['sub']
#                 )
#                 return user
#             else:
#                 social = SocialAccount.objects.get(unique_id=idinfo['sub'])
#                 return social.user
#         else:
#             raise ValueError("Incorrect Credentials")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
