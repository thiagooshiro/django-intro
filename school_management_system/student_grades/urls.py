# notas/urls.py

from django.urls import path
from .views import GradeListView, GradeCreateView, GradeDetailView, GradeDeleteView

urlpatterns = [
    path('', GradeListView.as_view(), name='grade_list'),  # GET para listar as notas
    path('create/', GradeCreateView.as_view(), name='grade_create'),  # POST para criar uma nota
    path('<int:pk>/', GradeDetailView.as_view(), name='grade_detail'),  # GET para ver os detalhes da nota
    path('<int:pk>/delete/', GradeDeleteView.as_view(), name='grade_delete'),  # DELETE para deletar a nota
]
