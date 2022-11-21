from django.db import models
from django.contrib.auth import get_user_model



class Aluno(models.Model):

    STATUS = (
        ('ativo','Ativo'),
        ('inativo', 'Inativo'),
    )   
    
    nome = models.CharField(max_length=255)
    telefone = models.IntegerField()
    email = models.EmailField()
    data_nascimento = models.DateField(null=True)
    description = models.TextField()
    status = models.CharField(max_length=8, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True) #boas praticas
    updated_at = models.DateTimeField(auto_now=True) #boas praticas
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
