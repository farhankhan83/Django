from django.contrib.auth.models import User
from django.db import models

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    date_of_birth = models.DateField(null=False)
    address = models.CharField(max_length=100, null=False)
    city_town = models.CharField(max_length=50, null=False)
    country = models.CharField(max_length=50, null=False)
    photo = models.ImageField(upload_to='student_photos', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Module(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    credit = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    availability = models.BooleanField(default=True)  # True for open, False for closed
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.name

class Registration(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    date_of_registration = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.module.name} ({self.date_of_registration})"
