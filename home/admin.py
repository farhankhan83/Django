from django.contrib import admin
from .models import Student, Module, Course, Category, Registration, Review
# Register your models here.

admin.site.register(Student)
admin.site.register(Module)
admin.site.register(Category)
admin.site.register(Registration)
admin.site.register(Course)
admin.site.register(Review)
