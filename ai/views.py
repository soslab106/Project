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
from .serializers import FileSerializer
from .models import File
from Project.settings import MEDIA_ROOT
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
import base64
from PIL import Image
import io
from django.http import HttpResponse

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
    return render(request, 'input_2.html', {'modelName':'FaceRecognition', 'actionName':'/face_recog_test/'})

def postCnnModels(request):
    if request.method == 'POST' and request.FILES['file']:
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        modelName = request.POST['modelName']
        if modelName == 'ResNet101' or modelName == 'VGG16':
            result = recogImgnet(uploaded_file_url, modelName)
        elif modelName == 'YOLOv3':
            recog_result = recogYOLOv3(uploaded_file_url)[0]
            MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media')
            result = MEDIA_ROOT+'\\{}-recog.jpg'.format(myfile.name[:myfile.name.rfind('.')])
            recog_result.save(result)
        elif modelName == 'Facenet':
            result = imageFaceDetec(uploaded_file_url, myfile)
        return result

def face_recog_test(request):
    if request.method == 'POST':
        file1 = request.FILES['file1']
        file2 = request.FILES['file2']
        fileR = request.FILES['fileR']
        fs = FileSystemStorage()
        file1name = fs.save(file1.name, file1)
        file2name = fs.save(file2.name, file2)
        fileRname = fs.save(fileR.name, fileR)
        learn_file_url = [fs.url(file1name), fs.url(file2name)]
        recog_file_url = fs.url(fileRname)
        nameList = [request.POST['name1'], request.POST['name2']]
        result = face_recognition_py(learn_file_url, nameList, recog_file_url)

        with open(result, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpg")

class FileView(APIView):
    parser_class = [FileUploadParser]

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
                im = Image.open(os.path.join(result))
                output = io.StringIO()
                im.save(output, "JPEG", quality=89)
                result = base64.b64encode(output.getvalue())
            return Response(result, status=status.HTTP_201_CREATED)
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
