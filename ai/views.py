from django.shortcuts import render
from .CNN.imgnet import recogImgnet
from .CNN.yolo import *
from .CNN.facenet import *
from django.core.files.storage import FileSystemStorage
import os
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import FileSerializer
from .models import File

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

def postCnnModels(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        modelName = request.POST['modelName']
        if modelName == 'ResNet101' or modelName == 'VGG16':
            result = recogImgnet(uploaded_file_url, modelName)
        elif modelName == 'YOLOv3':
            recog_result = recogYOLOv3(uploaded_file_url)
            result = []
            MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media')
            for each in recog_result:
                newFileName = MEDIA_ROOT+'\\{}-recog.jpg'.format(myfile.name[:myfile.name.rfind('.')])
                each.save(newFileName)
                result.append('/media/{}-recog.jpg'.format(myfile.name[:myfile.name.rfind('.')]))
        elif modelName == 'Facenet':
            result = imageFaceDetec(uploaded_file_url, myfile)
            
            # result = '/media/face.jpg'
        return render(request, 'result.html',{'result':result, 'modelName':modelName})

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
          return Response(file_serializer.data, status=status.HTTP_201_CREATED)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        file = self.get_object(pk)

        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
