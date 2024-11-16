from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Grade
from students.models import Student
from .models import Grade
from students.models import Student
from courses.models import Courses
from teachers.models import Teacher
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

@method_decorator(csrf_exempt, name='dispatch')
class GradeListView(View):
    # Listar todas as notas de um aluno
    def get(self, request, student_id=None, course_id=None):
        # Filtrar notas por aluno e/ou curso
        if student_id:
            grades = Grade.objects.filter(student_id=student_id)
        elif course_id:
            grades = Grade.objects.filter(course_id=course_id)
        else:
            grades = Grade.objects.all()

        # Convertendo as notas para um formato de resposta
        data = []
        for grade in grades:
            data.append({
                'student_id': grade.student.id,
                'course_id': grade.course.id,
                'teacher_id': grade.teacher.id,
                'grade': grade.grade,
                'evaluation_date': grade.evaluation_date,
                'evaluation_type': grade.evaluation_type,
                'remarks': grade.remarks,
            })

        return JsonResponse(data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class GradeDetailView(View):
    def get(self, request, grade_id):
        grade = get_object_or_404(Grade, id=grade_id)
        
        data = {
            'student_id': grade.student.id,
            'course_id': grade.course.id,
            'teacher_id': grade.teacher.id,
            'grade': grade.grade,
            'evaluation_date': grade.evaluation_date,
            'evaluation_type': grade.evaluation_type,
            'remarks': grade.remarks,
        }
        
        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class GradeCreateView(View):
    def post(self, request):
        data = json.loads(request.body)

        # Validação de dados
        errors = {}
        if 'student_id' not in data:
            errors['student_id'] = "Este campo é obrigatório."
        if 'course_id' not in data:
            errors['course_id'] = "Este campo é obrigatório."
        if 'teacher_id' not in data:
            errors['teacher_id'] = "Este campo é obrigatório."
        if 'grade' not in data or not isinstance(data['grade'], (int, float)):
            errors['grade'] = "A nota deve ser um número."
        if 'evaluation_date' not in data:
            errors['evaluation_date'] = "Este campo é obrigatório."
        if 'evaluation_type' not in data:
            errors['evaluation_type'] = "Este campo é obrigatório."

        if errors:
            return JsonResponse(errors, status=400)

        # Verificar se o aluno, curso e professor existem
        student = get_object_or_404(Student, id=data['student_id'])
        course = get_object_or_404(Courses, id=data['course_id'])
        teacher = get_object_or_404(Teacher, id=data['teacher_id'])


        # Validar se o professor leciona este curso
        if course != teacher.courses:  # Aqui checamos se o curso que o professor está tentando registrar é o mesmo que ele leciona
            return JsonResponse({'error': 'Você só pode emitir notas para a disciplina que leciona.'}, status=403)


        # Criar a nota
        grade = Grade.objects.create(
            student=student,
            course=course,
            teacher=teacher,
            grade=data['grade'],
            evaluation_date=data['evaluation_date'],
            evaluation_type=data['evaluation_type'],
            remarks=data.get('remarks', ''),
        )

        return JsonResponse({'id': grade.id}, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class GradeUpdateView(View):
    def put(self, request, grade_id):
        grade = get_object_or_404(Grade, id=grade_id)
        data = json.loads(request.body)

        # Validação de dados
        errors = {}
        if 'grade' in data and not isinstance(data['grade'], (int, float)):
            errors['grade'] = "A nota deve ser um número."

        if 'evaluation_date' in data and not data['evaluation_date']:
            errors['evaluation_date'] = "Este campo é obrigatório."

        if errors:
            return JsonResponse(errors, status=400)

        # Atualizar os campos fornecidos
        if 'grade' in data:
            grade.grade = data['grade']
        if 'evaluation_date' in data:
            grade.evaluation_date = data['evaluation_date']
        if 'remarks' in data:
            grade.remarks = data['remarks']

        grade.save()

        return JsonResponse({'id': grade.id}, status=200)
    
@method_decorator(csrf_exempt, name='dispatch')
class GradeDeleteView(View):
    def delete(self, request, grade_id):
        grade = get_object_or_404(Grade, id=grade_id)
        grade.delete()
        return JsonResponse({'message': 'Grade deleted'}, status=204)