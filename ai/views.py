from django.shortcuts import render
from .CNN.imgnet import recogImgnet
from .CNN.yolo import *
from .CNN.facenet import *
from .CNN.face_recog import *
from django.core.files.storage import FileSystemStorage
import os
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from .models import File
from Project.settings import MEDIA_ROOT
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
import base64
from PIL import Image
import io
from datauri import DataURI
from django.conf import settings 

from django.http import HttpResponse
from django.views.generic.edit import FormView
# Create your views here.
def renderIndex(request):
    return render(request, 'index.html')

def renderYolo(request):
    return render(request, 'input.html', {'modelName':'YOLOv3', 'actionName':'/postCnnModels/'})

def renderVgg(request):
    return render(request, 'input.html', {'modelName':'VGG16', 'actionName':'/postCnnModels/'})

def renderResNet(request):
    return render(request, 'input.html', {'modelName':'ResNet101', 'actionName':'/postCnnModels/'})

def renderFacenet(request):
    return render(request, 'input.html', {'modelName':'Facenet', 'actionName':'/postCnnModels/'})

def renderFaceRecog(request):
    return render(request, 'input_2.html', {'modelName':'FaceRecognition', 'actionName':'/TestUploadFile/'})

def postCnnModels(request):
    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        modelName = request.POST['modelName']
        if modelName == 'ResNet50' or modelName == 'VGG16':
            result = recogImgnet(uploaded_file_url, modelName)
        elif modelName == 'YOLOv3':
            recog_result = recogYOLOv3(uploaded_file_url)[0]
            MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media')
            result = MEDIA_ROOT+'\\{}-recog.jpg'.format(myfile.name[:myfile.name.rfind('.')])
            recog_result.save(result)
        elif modelName == 'Facenet':
            result = imageFaceDetec(uploaded_file_url, myfile)
        return result
 

class FileView(APIView):
    parser_class = [FileUploadParser]
    #permission_classes = (IsAuthenticated,)


    def get_object(self, pk):
        try:
            return File.objects.get(pk=pk)
        except File.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
            file = self.get_object(pk)
            serializer = FileSerializer(file)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        file_serializer = FileSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            result = postCnnModels(request)
            if request.POST['modelName']=='YOLOv3':
                result = DataURI.from_file(os.path.join(result))
            return Response({'result':result}, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        file = self.get_object(pk)
        os.remove(os.path.join(MEDIA_ROOT, file.file.name))
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LoginPage(TemplateView):
    template_name = 'login.html'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print("Errors", form.errors)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login/')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'register.html', context)


class TestUploadView(APIView):
    parser_class = (FileUploadParser, )
    #permission_classes = (IsAuthenticated,)
    queryset = File.objects.all()

    def post(self, request, *args, **kwargs):

        train_list = request.FILES.getlist('train') #訓練的圖片陣列
        print(train_list)
        test_list = request.FILES['test'] #偵測圖片
        print(test_list)
        fs = FileSystemStorage()
        train_list_url = []
        namelist = []
        
        for img in train_list:
            imgname = fs.save(img.name, img)
            train_list_url.append(fs.url(imgname))
            namelist.append(img.name.split('.')[0])
        imgname = fs.save(test_list.name, test_list)
        test_list_url = fs.url(imgname)

        #namelist = request.POST['name'] #訓練圖片的人名
        print(namelist)
        #name_list = namelist.split(',')
        name_list = namelist
        result = FaceRecognition(train_list_url, name_list, test_list_url)
        result = DataURI.from_file(result)
        return Response({'result':result}, status=status.HTTP_201_CREATED)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
# class GoogleLogin(TokenObtainPairView):
#     permission_classes = (AllowAny, ) # AllowAny for login
#     serializer_class = SocialLoginSerializer
#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             user = serializer.save()
#             return Response(get_tokens_for_user(user))
#         else:
#             raise ValueError('Not serializable')