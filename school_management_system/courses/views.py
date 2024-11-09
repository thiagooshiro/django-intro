# Create your views here.
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Courses
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class CoursesListView(View):
    # Listar todos os curos e suas descrições
    def get(self, request):
        courses = list(Courses.objects.values())
        return JsonResponse(courses, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CoursesCreateView(View):
    #Rota para cadastro de novos cursos
    def post(self, request):
        data = json.loads(request.body)

        # Validação manual
        errors = {}
        if 'name' not in data or not data['name']:
            errors['name'] = "Este campo é obrigatório."
        if 'description' not in data or not data['description']:
            errors['description'] = "Este campo é obrigatório."
        

        if errors:
            return JsonResponse(errors, status=400)

        # Criar o estudante
        course = Courses.objects.create(
            name=data['name'],
            description=data['description'],
        )


        return JsonResponse({'id': course.id,'name': course.name}, status=201)



@method_decorator(csrf_exempt, name='dispatch')
class CoursesDetailView(View):
    # Ver detalhes de um estudante específico, atualizar e deletar
    def get(self, request, course_id):
        course = get_object_or_404(Courses, id=course_id)
        data = {
            'id': course_id.id,
            'name': course.name,
            'description': course.description
            }
        return JsonResponse(data)

    def put(self, request, course_id):
        course = get_object_or_404(Courses, id=course_id)
        data = json.loads(request.body)

        # Validação manual
        errors = {}
        
        # Validação somente se o campo estiver presente na requisição
        if 'name' in data:
            if data['name'] == "":
                errors['name'] = "Este campo não pode ser vazio."

        if 'description' in data:
            if data['description'] == "":
                errors['descripion'] = "Este campo não pode ser vazio."

        if errors:
            return JsonResponse(errors, status=400)

        # Atualizar apenas os campos fornecidos
        if 'name' in data:
            course.name = data['name']
        if 'description' in data:
            course.description = data['description']

        course.save()

        return JsonResponse({'id': course.id, 'course': course.name}, status=200)

    def delete(self, request, course_id):
        course = get_object_or_404(Courses, id=course_id)
        course.delete()
        return JsonResponse({'message': 'Curso deletado'}, status=204)