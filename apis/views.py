#generic imports
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import GeeksSerializer,ImageUploadSerializer
from .models import GeeksModel
from rest_framework import generics
 
 #this is for image upload handeling
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
import base64

from django.core.files.uploadedfile import InMemoryUploadedFile
 #this is for image upload handeling

 # This is for LP - recognition
import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
 # This is for LP - recognition

 
###### geeks are only for testing!!!
# Create your views here.
class GeeksViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = GeeksModel.objects.all()
 
    # specify serializer to be used
    serializer_class = GeeksSerializer

class GeekDeleteSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = GeeksModel.objects.all()
    serializer_class = GeeksSerializer

    def perform_destroy(self, instance):
        # Perform any additional actions before deletion, if needed
        instance.delete()
    

class ImageUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwa2rgs):
        serializer = ImageUploadSerializer(data=request.data)

        if serializer.is_valid():
            image = serializer.validated_data['image']

            image_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
            img = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
            edged = cv2.Canny(bfilter, 30, 200)

            keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(keypoints)
            contours = sorted(contours,key=cv2.contourArea,reverse=True)[:10]

            location = None
            for countour in contours:
                approx = cv2.approxPolyDP(countour, 5, True)#set this 10 if it is not working
                if len(approx) == 4:
                    location=approx
                    break
            if location is None:
               return Response({"Error": "License Plate Not Found. Retry with different image."}, status = 400)

            mask = np.zeros(gray.shape, np.uint8)
            new_image = cv2.drawContours(mask, [location], 0, 255, -1)
            new_image = cv2.bitwise_and(img, img, mask=mask)

            (x, y) = np.where(mask==255)
            (x1, y1) = (np.min(x), np.min(y))
            (x2, y2) = (np.max(x), np.max(y))
            cropped_image = gray[x1:x2+1, y1:y2+1]

            reader = easyocr.Reader(['en'])
            result = reader.readtext(cropped_image)
            text = result[0][-2]

            return Response(text)
        else:
            return Response(serializer.errors,' 400 ', serializer,)