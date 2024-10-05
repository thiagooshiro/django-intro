from django.db import models


class Courses(models.Model):
    COURSE_CHOICES = [
        ('matematica', 'Matemática'),
        ('portugues', 'Português'),
        ('historia', 'História'),
        ('geografia', 'Geografia'),
        ('ciencias', 'Ciências'),
        ('ingles', 'Inglês'),
        ('ed_fisica', 'Educação Física'),
        ('artes', 'Artes'),
        ('literatura', 'Literatura'),
        ('quimica', 'Química'),
        ('fisica', 'Física'),
        ('biologia', 'Biologia'),
    ]


    name = models.CharField(max_length=100, choices=COURSE_CHOICES)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    enrollment_date = models.DateField(auto_now_add=True)
    courses = models.ManyToManyField(Courses, related_name='students')


    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.enrollment_date}"



