from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Student
import json
from datetime import datetime

@csrf_exempt
@require_http_methods(["GET"])
def student_list(request):
    students = list(Student.objects.values())
    return JsonResponse(students, safe=False)

@csrf_exempt
@require_http_methods(["GET"])
def student_detail(request, pk):
    try:
        student = Student.objects.get(pk=pk)
        return JsonResponse({
            'id': student.id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'birth_date': student.birth_date.isoformat(),
            'enrollment_date': student.enrollment_date.isoformat(),
            'email': student.email
        })
    except Student.DoesNotExist:
        return HttpResponseNotFound(json.dumps({"error": "Student not found"}))

@csrf_exempt
@require_http_methods(["POST"])
def student_create(request):
    try:
        data = json.loads(request.body)
        birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
        student = Student.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            birth_date=birth_date,
            email=data['email']
        )
        return JsonResponse({
            'id': student.id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'birth_date': student.birth_date.isoformat(),
            'enrollment_date': student.enrollment_date.isoformat(),
            'email': student.email
        }, status=201)
    except (KeyError, TypeError, ValueError) as e:
        return HttpResponseBadRequest(json.dumps({"error": str(e)}))

@csrf_exempt
@require_http_methods(["PUT"])
def student_update(request, pk):
    try:
        student = Student.objects.get(pk=pk)
        data = json.loads(request.body)
        if 'birth_date' in data:
            student.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
        student.first_name = data.get('first_name', student.first_name)
        student.last_name = data.get('last_name', student.last_name)
        student.email = data.get('email', student.email)
        student.save()
        return JsonResponse({
            'id': student.id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'birth_date': student.birth_date.isoformat(),
            'enrollment_date': student.enrollment_date.isoformat(),
            'email': student.email
        })
    except Student.DoesNotExist:
        return HttpResponseNotFound(json.dumps({"error": "Student not found"}))
    except (KeyError, TypeError, ValueError) as e:
        return HttpResponseBadRequest(json.dumps({"error": str(e)}))

@csrf_exempt
@require_http_methods(["DELETE"])
def student_delete(request, pk):
    try:
        student = Student.objects.get(pk=pk)
        student.delete()
        return JsonResponse({"message": "Student deleted successfully"})
    except Student.DoesNotExist:
        return HttpResponseNotFound(json.dumps({"error": "Student not found"}))
