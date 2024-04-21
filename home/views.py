from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages

def homePage(request):
    return render(request, 'homePage.html', {})

def aboutUs(request):
    return render(request, 'about.html', {})

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
    print(request)

    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']

        # Authentication Logic
        user = authenticate(request, useremail = email, password = password)
        if user is not None:
            login(request, user)
            message.success(request, 'User Logged In Successfully')
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