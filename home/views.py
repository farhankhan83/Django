from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def homePage(request):
    template = loader.get_template('homePage.html')
    return HttpResponse(template.render())

def aboutUs(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render())

def contact(request):
    template = loader.get_template('contact.html')
    return HttpResponse(template.render())