from django.shortcuts import render, get_object_or_404, redirect
from .models import Aluno, Event
from .forms import AlunoForm, EventForm
import uuid
from .google import createService, convertDatetime
service = createService()


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

def editAluno(request, id):
    aluno = get_object_or_404(Aluno, pk=id)
    form = AlunoForm(instance=aluno)

    if(request.method == 'POST'):
        form = AlunoForm(request.POST, instance=aluno)

        if(form.is_valid()):
            aluno.save()
            return redirect('/')
        else:
            return render(request, 'main/edit_aluno.html', {'form': form, 'aluno': aluno})
    else:
        return render(request, 'main/edit_aluno.html', {'form': form, 'aluno': aluno})

def deleteAluno(request, id):
    aluno = get_object_or_404(Aluno, pk=id)
    aluno.delete()
    return redirect('/')


def form_manual(request, id):
    aluno = get_object_or_404(Aluno, pk=id)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            nome_completo = aluno.nome
            email = aluno.email
            data_inicio = form.cleaned_data["data_inicio"]
            time_duration = form.cleaned_data["time_duration" ]
            recur = form.cleaned_data["recurrence"]
            dias = form.cleaned_data["qtd_dias"]
            summary = form.cleaned_data["summary"]
            description = form.cleaned_data["description"]
            
            recurrence = [f'RRULE:FREQ={recur};COUNT={dias};WKST=SU']
            request_id = str(uuid.uuid1())
            event_request_body = {
                'start': {
                    'dateTime': convertDatetime(data_inicio),
                    'timeZone': 'America/Sao_Paulo'
                },
                "end": {
                    'dateTime': convertDatetime(time_duration),
                    'timeZone': 'America/Sao_Paulo'
                },
                'summary': [summary],
                'description': [description],
                'colorID': 5,
                'status': 'confirmed',
                'transparency': 'opaque',
                'visibility': 'private',
                'location': 'Boa viagem',
                'recurrence': recurrence,  #
                'conferenceData': {'createRequest': {
                    'requestId': request_id,
                    "conferenceSolutionKey": {"type": "hangoutsMeet"}}},
                'attendees': [  # define os participantes
                    {
                        'displayName': nome_completo,
                        'comment': 'Assistir aula.',
                        'email': email,
                        'optional': True,
                        'organizer': True,
                        'responseStatus': 'accepted'
                    },
                ],
                'creator': {
                    "id": 'Carlos',
                    "email": 'carloscelestino93@gmail.com',
                    "displayName": 'Carlos C.',
                    "self": True
                },
                'organizer': {
                    "id": 'Carlos',
                    "email": 'carloscelestino93@gmail.com',
                    "displayName": 'Carlos C.',
                    "self": True
                }
            }
            maxAttendees = 3
            sendNotifications = True
            sendUpdates = 'none'
            supportsAttachments = True

            response = service.events().insert(
                calendarId='primary',
                maxAttendees=maxAttendees,
                sendNotifications=sendNotifications,  # envia notificações para os participantes.
                sendUpdates=sendUpdates,
                supportsAttachments=supportsAttachments,
                conferenceDataVersion=1,
                body=event_request_body
            ).execute()
            evento = Event()
            evento.event = response['id']
            evento.aluno_id = id
            evento.save()
            return redirect('/')
       
    else:
        form = EventForm()
        return render(request, 'main/add_aluno.html', {'form': form})



def eventView(request, id):
    evento = Event.objects.filter(aluno_id=id)
    lista_sumario = []
    lista_eventos = []
    for e in evento:
        event = service.events().get(calendarId='primary', eventId=e).execute()
        eventSummary = event['summary']
        event_id = event['id']
        lista_sumario.append({'id': event_id, 'summary':eventSummary})
    return render(request, 'eventos/evento_list.html', {'evento': event, 'eventSummary': eventSummary,
     'lista_sumario':lista_sumario, 'lista_eventos':lista_eventos, 'event_id':event_id})

def delete_event(request, event):
    evento = get_object_or_404(Event,event=event)
    service.events().delete(calendarId='primary', eventId=evento).execute()
    deletar_evento = get_object_or_404(Event, event=evento)
    deletar_evento.delete()
    return redirect('/')