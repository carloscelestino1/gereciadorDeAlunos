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


class EventForm(forms.Form):

    data_inicio = forms.DateTimeField(
        label='Início do evento',
        widget=forms.DateTimeInput(
            format='%Y-%m-%d T%H:%M',
            attrs={
                'type': 'datetime-local',
            }),
        input_formats=('%Y-%m-%d T%H:%M',))

    time_duration = forms.DateTimeField(
        label='Fim do evento',
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={
                'type': 'datetime-local',
            }),
        input_formats=('%Y-%m-%dT%H:%M',))
    
    Options = (
        ('DAILY', 'DAILY'),
        ('WEEKLY', 'WEEKLY'),
        ('MONTHLY', 'MONTHLY'),
     )
    recurrence = forms.ChoiceField(
        label='Recorrencia', 
        widget=forms.Select, choices=Options)

    Options = (
        ('1', '01'),
        ('2', '02'),
        ('3', '03'),
        ('4', '04'),
        ('5', '05'),
     )
    qtd_dias = forms.ChoiceField(
        label='Numero de repetições', 
        widget=forms.Select, choices=Options)
    summary = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255)


    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        data_inicio = cleaned_data.get("data_inicio")
        time_duration = cleaned_data.get("time_duration")
        recurrence = cleaned_data.get("recurrence")
        qtd_dias = cleaned_data.get("qtd_dias")
        summary = cleaned_data.get("summary")
        description = cleaned_data.get("description")

        class Meta:
            model = Aluno()

            fields = ['nome', 'description', 'telefone', 'email', 'data_nascimento']