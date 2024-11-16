from django.http import JsonResponse
from django.views import View
from .models import Teacher
from courses.models import Courses
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404


@method_decorator(csrf_exempt, name='dispatch')
class TeacherListView(View):
    # Listar todos os professores
    def get(self, request):
        teachers = list(Teacher.objects.values())
        return JsonResponse(teachers, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class TeacherCreateView(View):
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
        elif Teacher.objects.filter(email=data['email']).exists():
            errors['email'] = "Este email já está cadastrado."
        if 'birth_date' not in data or not data['birth_date']:
            errors['birth_date'] = "Este campo é obrigatório."
        if 'hiring_date' not in data or not data['hiring_date']:
            errors['hiring_date'] = "Este campo é obrigatório."
        if 'salary' not in data or not data['salary']:
            errors['salary'] = "Este campo é obrigatório."
        if 'courses' not in data or not data['courses']:
            errors['courses'] = "Este campo é obrigatório."

        if errors:
            return JsonResponse(errors, status=400)

        # Valida o curso antes de criar o professor
        try:
            course = Courses.objects.get(id=data['courses'])  # Espera um único ID
        except Courses.DoesNotExist:
            return JsonResponse({'courses': "Curso não encontrado."}, status=400)

        # Criar o professor
        teacher = Teacher.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            birth_date=data['birth_date'],
            hiring_date=data['hiring_date'],
            salary=data['salary'],
            courses=course,  # Associar o curso diretamente
        )

        return JsonResponse({'id': teacher.id}, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class TeacherDetailView(View):
    # Ver detalhes de um professor específico
    def get(self, request, teacher_id):
        teacher = get_object_or_404(Teacher, id=teacher_id)
        data = {
            'id': teacher.id,
            'first_name': teacher.first_name,
            'last_name': teacher.last_name,
            'email': teacher.email,
            'birth_date': teacher.birth_date,
            'hiring_date': teacher.hiring_date,
            'salary': teacher.salary,
        }
        return JsonResponse(data)

    # Atualizar um professor existente
    def put(self, request, teacher_id):
        teacher = get_object_or_404(Teacher, id=teacher_id)
        data = json.loads(request.body)

        # Validação manual
        errors = {}

        if 'first_name' in data and data['first_name'] == "":
            errors['first_name'] = "Este campo não pode ser vazio."

        if 'last_name' in data and data['last_name'] == "":
            errors['last_name'] = "Este campo não pode ser vazio."

        if 'email' in data:
            if data['email'] == "":
                errors['email'] = "Este campo não pode ser vazio."
            elif Teacher.objects.exclude(id=teacher_id).filter(email=data['email']).exists():
                errors['email'] = "Este email já está cadastrado."

        if 'birth_date' in data and data['birth_date'] == "":
            errors['birth_date'] = "Este campo não pode ser vazio."

        if 'hiring_date' in data and data['hiring_date'] == "":
            errors['hiring_date'] = "Este campo não pode ser vazio."

        if 'salary' in data and data['salary'] == "":
            errors['salary'] = "Este campo não pode ser vazio."

        if errors:
            return JsonResponse(errors, status=400)

        # Atualizar somente os campos fornecidos
        if 'first_name' in data:
            teacher.first_name = data['first_name']
        if 'last_name' in data:
            teacher.last_name = data['last_name']
        if 'email' in data:
            teacher.email = data['email']
        if 'birth_date' in data:
            teacher.birth_date = data['birth_date']
        if 'hiring_date' in data:
            teacher.hiring_date = data['hiring_date']
        if 'salary' in data:
            teacher.salary = data['salary']
        
        teacher.save()

        return JsonResponse({'id': teacher.id}, status=200)

    # Deletar um professor
    def delete(self, request, teacher_id):
        teacher = get_object_or_404(Teacher, id=teacher_id)
        teacher.delete()
        return JsonResponse({'message': 'Teacher deleted'}, status=204)
