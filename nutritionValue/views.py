from django.shortcuts import render
from django.http import QueryDict
from rest_framework import viewsets, status, permissions
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response

class NutritionValueViewSet():
    def create(self, request, *args, **kwargs):
        if request.content_type == 'multipart/form-data':
            pass
        elif request.content_type == 'application/json':
            # get the data from the request
            data = request.data
            print(data)