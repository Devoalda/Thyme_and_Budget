from django.shortcuts import render
from django.http import QueryDict
from rest_framework import viewsets, status, permissions
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response

class NutritionValueViewSet(viewsets.ViewSet):
    # POST
    def create(self, request, *args, **kwargs):
        pass

    # GET a list of all nutrition values
    def list(self, request, *args, **kwargs):
        pass

    # GET a single nutrition value
    def retrieve(self, request, pk=None, *args, **kwargs):
        pass