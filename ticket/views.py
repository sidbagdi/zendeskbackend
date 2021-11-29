import base64
import configparser
import os
import requests
from django.shortcuts import render
import datetime
from ticket.models import Ticket
from ticket.tables import TicketTable


def getAllTickets(request):
    config = get_config('app.ini')
    text = config['DEFAULT']['email_id']+"/"+config['DEFAULT']['api_token']
    base64_bytes = base64.b64encode(text.encode('ascii'))
    token = base64_bytes.decode('ascii')
    endpoint = config['DEFAULT']['api_url']+config['DEFAULT']['all_tickets_url']
    headers = {'Content-Type': 'application/json', "Authorization": "Basic " + str(token), 'Accept': 'application/json'}
    try:
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200 :
            print("NO ERROR")
            for ticket in Ticket.objects.all():
                Ticket.objects.get(id=ticket.id).delete()

            for ticket in response.json()['tickets']:
                create_ticket_object(ticket)

            return None
        else:
            print("ERROR")
            return render(request, 'ticket/ApiError.html')
    except:
        print("Exception")
        return 1
def get_config(file_name):
    path = os.path.dirname(os.path.realpath(__file__))
    config_dir = '/'.join([path, file_name])
    config = configparser.ConfigParser()
    config.read(config_dir)
    return config

def detail(request, ticket_id):
    config = get_config('app.ini')
    text = config['DEFAULT']['email_id'] + "/" + config['DEFAULT']['api_token']
    base64_bytes = base64.b64encode(text.encode('ascii'))
    token = base64_bytes.decode('ascii')
    endpoint = config['DEFAULT']['api_url'] + config['DEFAULT']['single_ticket_url']+"/" + str(ticket_id)
    headers = {'Content-Type': 'application/json', "Authorization": "Basic " + str(token), 'Accept': 'application/json'}
    response = requests.get(endpoint, headers=headers)
    print(response)
    return response

def index(request):
    return render(request, 'ticket/landing.html')


def search(request):
    if request.method == 'POST':
        search_id = request.POST.get('id', None)
        print("User requested", search_id)
        try:
            if str(search_id).isnumeric() and Ticket.objects.filter(id=search_id).exists():
                ticket = Ticket.objects.get(id = search_id)

            else:
                response = detail(request, search_id)
                if response.status_code==200 and response.json()['ticket']:
                    create_ticket_object(response.json()['ticket'])
                elif response.status_code in (400,404,401, 500):
                    return render(request, 'ticket/TicketNotFound.html')
                else:
                    print(response.status_code)
                    return render(request, 'ticket/ApiError.html')

            return render(request, 'ticket/ticket.html', context={'ticket': ticket})
        except Ticket.DoesNotExist:
            return render(request, 'ticket/TicketNotFound.html')
    else:
        return render(request, 'ticket/landing.html')

def create_ticket_object(ticket_json):
    ticket = Ticket()
    ticket.assignee_id = ticket_json['assignee_id']
    ticket.id = ticket_json['id']
    ticket.external_id = ticket_json['external_id']
    ticket.group_id = ticket_json['group_id']
    ticket.organization_id = ticket_json['organization_id']
    ticket.created_at = datetime.datetime.strptime(ticket_json['created_at'], "%Y-%m-%dT%H:%M:%SZ")
    ticket.updated_at = datetime.datetime.strptime(ticket_json['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
    ticket.type = ticket_json['type']
    ticket.subject = ticket_json['subject']
    ticket.raw_subject = ticket_json['raw_subject']
    ticket.description = ticket_json['description']
    ticket.priority = ticket_json['priority']
    ticket.status = ticket_json['status']
    ticket.recipient = ticket_json['recipient']
    ticket.status = ticket_json['status']
    ticket.requester_id = ticket_json['requester_id']
    ticket.submitter_id = ticket_json['submitter_id']
    ticket.assignee_id = ticket_json['assignee_id']
    ticket.due_at = ticket_json['due_at']
    ticket.tags = ticket_json['tags']

    ticket.save()


# class TicketListView(SingleTableView):
#
#     model = Ticket
#     table_class = TicketTable
#     queryset = Ticket.objects.all()
#     template_name = 'ticket/allTickets.html'

def ticket_listing(request):
    x=getAllTickets(request)
    if x==1:
        return render(request, 'ticket/ApiError.html')
    table = TicketTable(Ticket.objects.all())
    table.paginate(page=request.GET.get("page", 1), per_page=25)
    return render(request, "ticket/allTickets.html", {"table": table})