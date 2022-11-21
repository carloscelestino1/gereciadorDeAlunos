from django import forms
from .models import Aluno


class AlunoForm(forms.ModelForm):
    data_nascimento = forms.DateField(
        widget=forms.TextInput(
            attrs={"type":"date"}
        )
    )
    class Meta:
        model = Aluno
        fields = ('nome', 'description', 'telefone', 'email', 'data_nascimento')