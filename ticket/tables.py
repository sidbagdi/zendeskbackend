import django_tables2 as tables

from ticket.models import Ticket


class TicketTable(tables.Table):

    class Meta:
        model = Ticket
        template_name = "django_tables2/bootstrap-responsive.html"
        attrs = {'class': 'table table-striped table-hover'}
        fields = ('id', 'created_at', 'description', 'status','priority','requester_id')
        sequence = ('id', 'created_at', 'description', 'status','priority','requester_id')

