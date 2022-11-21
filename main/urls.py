from django.urls import path
from . import views

urlpatterns = [
    path('', views.alunoView, name='aluno-lista'),
    path('aluno/<int:id>', views.alunoIDview, name="aluno-view"),
    path('newaluno/', views.newAluno, name="new-aluno"),
]
