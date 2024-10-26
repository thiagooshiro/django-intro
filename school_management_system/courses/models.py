from django.db import models

class Courses(models.Model):
    COURSE_CHOICES = [
        ('matematica', 'Matemática'),
        ('portugues', 'Português'),
        ('historia', 'História'),
        ('geografia', 'Geografia'),
        ('ciencias', 'Ciências'),
        ('ingles', 'Inglês'),
        ('ed_.fisica', 'Educação Física'),
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

