from django.db import models
from students.models import Student
from courses.models import Courses
from teachers.models import Teacher

class Grade(models.Model):
    # Definindo as escolhas possíveis para o tipo de avaliação
    EVALUATION_TYPES = [
        ('EXAM', 'Prova'),
        ('ASSIGNMENT', 'Trabalho'),
        ('PARTICIPATION', 'Participação'),
        ('QUIZ', 'Quiz'),
        ('FINAL', 'Prova Final'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='grades')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='grades')
    grade = models.DecimalField(max_digits=5, decimal_places=2)  # Ex.: 7.50
    evaluation_date = models.DateField()
    remarks = models.TextField(null=True, blank=True)
    evaluation_type = models.CharField(
        max_length=15, 
        choices=EVALUATION_TYPES, 
        default='EXAM'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course', 'evaluation_date', 'evaluation_type'], 
                name='unique_grade_per_evaluation'
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.course} - {self.grade} ({self.evaluation_type})"
