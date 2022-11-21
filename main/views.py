from django.shortcuts import render, get_object_or_404, redirect
from .models import Aluno
from .forms import AlunoForm

def alunoView(request):
    alunos = Aluno.objects.all()
    return render(request, 'main/list.html', {'alunos':alunos})

def alunoIDview(request, id):
    aluno = get_object_or_404(Aluno, pk=id)
    return render(request, 'main/aluno.html', {'aluno': aluno})

def newAluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        
        if form.is_valid():
            aluno = form.save(commit=False)
            aluno.status = 'ativo'
            aluno.user = request.user
            aluno.save()
            return redirect('/')
    else:
        form = AlunoForm()
    return render(request, 'main/add_aluno.html', {'form': form})