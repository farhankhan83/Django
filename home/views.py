from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from .forms import RegisterForm
from .models import Course, Module

def homePage(request):
    return render(request, 'homePage.html', {})

def aboutUs(request):
    return render(request, 'about.html', {})

def courses(request):
    courses = Course.objects.values('id', 'name', 'description')
    print(courses)
    return render(request, 'courses.html', {'courses': courses})

def courseDetail(request, course_id):
    course = Course.objects.get(id=course_id)
    modules = Module.objects.filter(courses__id=course_id)
    return render(request, 'courses_detail.html', {'course': course, 'modules': modules})

def contact(request):
    return render(request, 'contact.html', {})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authentication Logic
        user = authenticate(request, username = username, password = password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'User Logged In Successfully')
            return redirect('Home')
        else:
            messages.success(request, "Error Logging In")
            return redirect('Home')
    else:
        return render(request, 'login.html', {})


def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authentication Logic
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, 'User Logged In Successfully')
            return redirect('Home')
        else:
            messages.success(request, "Error Logging In")
            return redirect('Home')
    else:
        return render(request, 'home.html', {})

def logoutUser(req):
    logout(req)
    messages.success(req, 'Logged out successfully!')
    return redirect('Home')


def register_student(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Authenticate and logg user in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username = username, password = password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'User Registered  Successfully')
                return redirect('Home')
        else:
            for err_msg in form.error_messages:
                messages.error(request, err_msg)
            return render(request, 'register.html', {'form': form })
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form })
