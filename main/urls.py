from django.urls import path
from . import views

urlpatterns = [
    path('', views.alunoView, name='aluno-lista'),
    path('aluno/<int:id>', views.alunoIDview, name="aluno-view"),
    path('newaluno/', views.newAluno, name="new-aluno"),
    path('edit/<int:id>', views.editAluno, name="edit-aluno"),
    path('delete/<int:id>', views.deleteAluno, name="delete-aluno"),
    path('event/<int:id>', views.form_manual, name="event-aluno"),
    path('eventId/<int:id>', views.eventView, name="event-aluno"),
    path('deleteevent/<str:event>', views.delete_event, name="delete-event"),
]
