from django.db import models
from courses.models import Courses

class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    courses = models.ForeignKey(Courses, on_delete=models.DO_NOTHING, related_name='teachers')
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=True)
    birth_date = models.DateField()
    hiring_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def age(self):
        # Método para calcular a idade do professor com base na data de nascimento
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def years_of_service(self):
        # Método para calcular o tempo de serviço com base na data de contratação
        from datetime import date
        today = date.today()
        return today.year - self.hiring_date.year - ((today.month, today.day) < (self.hiring_date.month, self.hiring_date.day))
