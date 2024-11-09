from django.urls import path
from .views import CoursesListView, CoursesCreateView , CoursesDetailView 

urlpatterns = [
    path('', CoursesListView.as_view(), name='courses_list'),
    path('create/', CoursesCreateView.as_view(), name='courses_create'),  # POST para criar estudante
    path('<int:course_id>/', CoursesDetailView.as_view(), name='courses_detail'),
]
