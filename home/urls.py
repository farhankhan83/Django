from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.homePage, name='Home'),
    path('about', views.aboutUs, name='About'),
    path('courses', views.courses, name='Courses'),
    path('courses/<int:course_id>', views.courseDetail, name='CourseDetail'),
    path('modules/<int:module_id>', views.moduleDetail, name='ModuleDetail'),
    path('contact', views.contact, name='Contact'),
    path('login', views.login, name='Login'),
    path('logout', views.logoutUser, name='Logout'),
    path('register', views.register_student, name='RegisterStudent'),
    path('register_in_module/<int:module_id>', views.register_in_module, name='RegisterModule'),
    path('student', views.student_profile, name='StudentProfile'),
    path('edit_student', views.edit_profile, name='EditProfile'),
    path('<int:id>/password/', auth_views.PasswordChangeView.as_view(template_name='change-password.html'), name='Password'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),

]