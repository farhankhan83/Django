from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='Home'),
    path('about/', views.aboutUs, name='About'),
    path('courses/', views.courses, name='Courses'),
    path('courses/<int:course_id>', views.courseDetail, name='CourseDetail'),
    path('modules/<int:module_id>', views.moduleDetail, name='ModuleDetail'),
    path('contact/', views.contact, name='Contact'),
    path('login', views.login, name='Login'),
    path('logout/', views.logoutUser, name='Logout'),
    path('register/', views.register_student, name='RegisterStudent'),
    path('register_in_module/<int:module_id>', views.register_in_module, name='RegisterModule'),
]