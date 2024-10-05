from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Student
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class StudentListView(View):
    # Listar todos os estudantes e cadastrar novos estudantes
    def get(self, request):
        students = list(Student.objects.values())
        return JsonResponse(students, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class StudentCreateView(View):
    def post(self, request):
        data = json.loads(request.body)

        # Validação manual
        errors = {}
        if 'first_name' not in data or not data['first_name']:
            errors['first_name'] = "Este campo é obrigatório."
        if 'last_name' not in data or not data['last_name']:
            errors['last_name'] = "Este campo é obrigatório."
        if 'email' not in data or not data['email']:
            errors['email'] = "Este campo é obrigatório."
        elif Student.objects.filter(email=data['email']).exists():
            errors['email'] = "Este email já está cadastrado."
        if 'date_of_birth' not in data or not data['date_of_birth']:
            errors['date_of_birth'] = "Este campo é obrigatório."
        if 'courses' not in data:
            errors['courses'] = "Este campo é obrigatório."

        if errors:
            return JsonResponse(errors, status=400)

        # Criar o estudante
        student = Student.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            date_of_birth=data['date_of_birth'],
        )

        # Assumindo que 'courses' é uma lista de IDs
        if 'courses' in data:
            student.courses.set(data['courses'])

        return JsonResponse({'id': student.id}, status=201)



@method_decorator(csrf_exempt, name='dispatch')
class StudentDetailView(View):
    # Ver detalhes de um estudante específico, atualizar e deletar
    def get(self, request, student_id):
        student = get_object_or_404(Student, id=student_id)
        data = {
            'id': student.id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'date_of_birth': student.date_of_birth,
            'email': student.email,
            'courses': list(student.courses.values_list('name', flat=True)),  # Listar cursos matriculados
        }
        return JsonResponse(data)

    def put(self, request, student_id):
        student = get_object_or_404(Student, id=student_id)
        data = json.loads(request.body)

        # Validação manual
        errors = {}
        
        # Validação somente se o campo estiver presente na requisição
        if 'first_name' in data:
            if data['first_name'] == "":
                errors['first_name'] = "Este campo não pode ser vazio."

        if 'last_name' in data:
            if data['last_name'] == "":
                errors['last_name'] = "Este campo não pode ser vazio."

        if 'email' in data:
            if data['email'] == "":
                errors['email'] = "Este campo não pode ser vazio."
            elif Student.objects.exclude(id=student_id).filter(email=data['email']).exists():
                errors['email'] = "Este email já está cadastrado."

        if 'date_of_birth' in data:
            if data['date_of_birth'] == "":
                errors['date_of_birth'] = "Este campo não pode ser vazio."

        # Validação simples para cursos (se necessário)
        if 'courses' in data and not isinstance(data['courses'], list):
            errors['courses'] = "Cursos devem ser uma lista."

        if errors:
            return JsonResponse(errors, status=400)

        # Atualizar apenas os campos fornecidos
        if 'first_name' in data:
            student.first_name = data['first_name']
        if 'last_name' in data:
            student.last_name = data['last_name']
        if 'email' in data:
            student.email = data['email']
        if 'date_of_birth' in data:
            student.date_of_birth = data['date_of_birth']
        
        student.save()

        # Atualizando cursos se fornecido
        if 'courses' in data:
            student.courses.set(data['courses'])

        return JsonResponse({'id': student.id}, status=200)

    def delete(self, request, student_id):
        student = get_object_or_404(Student, id=student_id)
        student.delete()
        return JsonResponse({'message': 'Student deleted'}, status=204)
