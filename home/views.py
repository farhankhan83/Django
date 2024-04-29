from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.core.mail import send_mail
from .forms import RegisterForm, UserStudentEditForm, ContactForm, ReviewForm, ProfilePictureForm
from .models import Course, Module, Student, Registration, Review
from django.contrib.auth.decorators import login_required
from app.settings import EMAIL_HOST_USER, EMAIL_RECEPIENT

def homePage(request):
    courses = Course.objects.values('id', 'name', 'description')[:3]
    return render(request, 'homePage.html', {'courses': courses})

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

def moduleDetail(request, module_id):
    if request.method == 'POST':
        form = ReviewForm(request.user.id, module_id, request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ReviewForm(request.user.id,module_id)

    modules = Module.objects.get(id=module_id)
    registrations = Registration.objects.filter(module_id=module_id)
    # Get the user IDs of registered students
    user_ids = registrations.values_list('student_id', flat=True)

    registered_students = Student.objects.filter(user_id__in=user_ids).select_related('user')
    reviews = Review.objects.filter(module_id=module_id).select_related('student')
    current_student_review = None
    for review in reviews:
        if review.student.id == request.user.id:
            current_student_review = True
        review.stars = generate_stars(review.rating)
    if current_student_review == True:
        form = None

    found_user = None
    for student in registered_students:
        if student.user.id == request.user.id:
            found_user = True
            break
    return render(request, 'module_detail.html', {'modules': modules, 'students': registered_students, 'isStudentRegistered': found_user, 'reviews': reviews, 'reviewForm': form})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            send_mail(
                subject=subject,
                message=f'Name: {name}\nEmail: {email}\nMessage: {message}',
                from_email=EMAIL_HOST_USER,  # Use your email settings or leave None to use the DEFAULT_FROM_EMAIL setting
                recipient_list=[EMAIL_RECEPIENT],  # Replace with your email address
                fail_silently=False,
            )
            return redirect('Contact')  # Render a success page
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

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
            return redirect('Login')
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
        print(form.errors)
        if form.is_valid():
            created_user = form.save()
            student = Student.objects.create(
                date_of_birth = form.cleaned_data['date_of_birth'],
                address = form.cleaned_data['address'],
                city_town = form.cleaned_data['city'],
                country = form.cleaned_data['country'],
                photo = form.cleaned_data['photo'],
                user = created_user,
            )
            # Authenticate and logg user in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username = username, password = password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Student Registered Successfully')
                return redirect('Home')
        else:
            for err_msg in form.error_messages:
                messages.error(request, err_msg)
            return render(request, 'register.html', {'form': form })
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form })

def register_in_module(request, module_id):
    module = Module.objects.get(id=module_id)
    if request.method == 'POST':
        # Check if the action is to register or unregister
        action = request.POST.get('action')

        if action == 'register':
            student_id = request.user.id
            # Check if the student is already registered
            if Registration.objects.filter(student_id=student_id, module_id=module_id).exists():
                messages.error(request, 'Student is already registered for this module.')
            else:
                # Create a registration record
                Registration.objects.create(student_id=student_id, module_id=module_id)
                messages.success(request, 'Student registered successfully.')
        elif action == 'unregister':
            student_id = request.user.id
            # Check if the student is registered for this module
            registration = Registration.objects.filter(student_id=student_id, module_id=module_id).first()
            if registration:
                registration.delete()
                messages.success(request, 'Student unregistered successfully.')
            else:
                messages.error(request, 'Student is not registered for this module.')
        
        # Redirect back to the module detail page
        return moduleDetail(request=request, module_id=module_id)

    else:
        # If it's not a POST request, render the module detail page
        return moduleDetail(request=request, module_id=module_id)

@login_required(login_url='/')
def student_profile(request):
    form = ProfilePictureForm()
    user_id = request.user.id
    student = Student.objects.select_related('user').get(user_id=user_id)
    if student is None:
        return redirect('Home')
    
    student_registrations = Registration.objects.filter(student_id=user_id).select_related('module')
    # Redirect back to the module detail page
    return render(request, 'student_profile.html', {'student': student, 'student_registrations': student_registrations, 'profilePictureForm': form})

@login_required(login_url='/')
def edit_profile(request):
    student = Student.objects.get(user=request.user)

    print({'date_of_birth': student.date_of_birth,
                                                            'address': student.address,
                                                            'city_town': student.city_town,
                                                            'country': student.country,
                                                            'photo': student.photo})
    if request.method == 'POST':
        form = UserStudentEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('StudentProfile')
    else:
        form = UserStudentEditForm(instance=request.user, initial={'date_of_birth': student.date_of_birth,
                                                            'address': student.address,
                                                            'city_town': student.city_town,
                                                            'country': student.country,
                                                            'photo': student.photo})

    return render(request, 'edit_profile.html', {'form': form})

def generate_stars(rating):
    filled_stars = ['filled' for _ in range(rating)]
    empty_stars = ['empty' for _ in range(5 - rating)]
    return filled_stars + empty_stars


def submit_review(request, module_id):
    if request.method == 'POST':
        form = ReviewForm(module_id, request.POST)
        if form.is_valid():
            form.save()
            return redirect('Home')  # Render a success page
    else:
        form = ReviewForm(module_id)
    return render(request, 'module_detail.html', {'form': form})


@login_required
def update_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.student)
        print(form.is_valid())
        if form.is_valid():
            photo = request.FILES['photo']
            print(request.user.student.photo)
            request.user.student.photo = photo
            request.user.student.save()
            messages.success(request, 'Image Updated Successfully')
        else:
            messages.error(request, 'Fail to update the image')
    return student_profile(request=request)
    
