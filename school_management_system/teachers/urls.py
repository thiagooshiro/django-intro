from django.urls import path
from .views import TeacherListView, TeacherCreateView , TeacherDetailView 

urlpatterns = [
    path('', TeacherListView.as_view(), name='teachers_list'),
    path('create/', TeacherCreateView.as_view(), name='teachers_create'),  # POST para criar estudante
    path('<int:teacher_id>/', TeacherDetailView.as_view(), name='teachers_detail'),
]
