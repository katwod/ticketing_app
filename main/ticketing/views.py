import mimetypes
import os
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Ticket

# Create your views here.
User = get_user_model()


def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username, password = password)

        if user is not None:
            auth.login(request, user)
            if user.assistant.team == "DZ":
                #return AssistanteDZ(request)
                return HttpResponseRedirect("/assistanteDZ")
            elif user.assistant.team == "FR":
                #return AssistanteFR(request)
                return HttpResponseRedirect("/assistanteFR")
        else :
            messages.info(request, 'Credentials are invalid please try again.')
            return redirect('login')
        
    else :
        return render(request, 'login.html')


def AssistanteDZ(request):
    #tickets = Ticket.objects.all()
    user_id = request.user.id
    tickets = Ticket.objects.order_by('-created_on')

    context = {
        'tickets' : tickets,
        'user_id' : user_id
    }
    return render(request, 'assistanteDZ.html', context)


def AssignTicket(request):
    try :
        ticket = Ticket.objects.get(pk=request.POST["ticket_id"])
        user = User.objects.get(pk=request.POST["assignee_id"])
        ticket.assigned_to = user
        ticket.status = 'assigned'
        ticket.save()
    
    except Exception as e:
        messages.error(request,e)
        return HttpResponseRedirect("/assistanteDZ")

    return HttpResponseRedirect("/assistanteDZ")

def AssistanteFR(request):
    tickets = Ticket.objects.all()
    return render(request, 'assistanteFR.html', {'tickets' : tickets})


def ticket_by_id(request, ticket_id):
    user = request.user
    ticket = Ticket.objects.get(pk=ticket_id)
    
    context = {
        'ticket' : ticket,
        'user' : user
    }
    
    return render(request, 'ticket_by_id.html', context)


def ticketComplete(request, ticket_id):
    user_id = request.user.id
    ticket = Ticket.objects.get(pk=ticket_id)
    
    context = {
        'ticket' : ticket,
        'user_id' : user_id
    }
    
    return render(request, 'completeTicket.html', context)


def newTicketCreation(request):
    if request.method == "POST":
        Ticket.objects.create(
            author = request.user,
            status = 'Pending',
            title = request.POST.get('title'), 
            description = request.POST.get('description'),
            contextual_info = request.POST.get('contextual_info'),
            deadline = request.POST.get('deadline')
        )
    return HttpResponseRedirect("/assistanteFR")


def openCreateForm (request):
    return render (request, 'newTicket.html')


def filterTickets(request):
    status = request.GET.get('status')
    if status == 'all':
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(status=status)

    return render(request, 'assistanteFR.html', {'tickets' : tickets})

def openUploadForm(request):
    ticketId = request.POST.get("ticket_id")
    ticket = Ticket.objects.get(pk=ticketId)
    if request.method == "POST":
        ticket.status = "Completed"
        ticket.notes = request.POST.get("notes")
        ticket.files = request.FILES.get("file")
        ticket.save()
    return HttpResponseRedirect("/assistanteDZ")


def downloadFile(request):
    ticketId = request.GET.get("ticket_id") 
    print("ticketId -->", ticketId)
    ticket = Ticket.objects.get(pk=ticketId)

    fileDownloadPath = str(ticket.files)
    if os.path.exists(fileDownloadPath):
        with open(fileDownloadPath,  'rb')as fh:
            response=HttpResponse(fh.read(),content_type="application/adminupload")
            response['Content-Disposition']='inline;filename='+os.path.basename(fileDownloadPath)
            return response
    raise Http404