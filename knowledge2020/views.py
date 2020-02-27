from django.shortcuts import render, redirect
from django.http import HttpResponse
from .serializers import *
import requests

# Create your views here.

def index(request):
    return HttpResponse("Main page for Knowledge 2020")
