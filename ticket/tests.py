
from django.test import TestCase
import configparser
from unittest.mock import patch

from ticket.models import Ticket
from ticket.views import getAllTickets, detail


class MockIndividualTicket:
    def __init__(self):
        self.status_code = 200

    def json(self):
        return {'ticket': {'url': 'https://zccsiddharth.zendesk.com/api/v2/tickets/3.json', 'id': 3, 'external_id': None, 'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2021-11-28T09:27:18Z', 'updated_at': '2021-11-28T09:27:18Z', 'type': None, 'subject': 'excepteur laborum ex occaecat Lorem', 'raw_subject': 'excepteur laborum ex occaecat Lorem', 'description': 'Exercitation amet in laborum minim. Nulla et veniam laboris dolore fugiat aliqua et sit mollit. Dolor proident nulla mollit culpa in officia pariatur officia magna eu commodo duis.\n\nAliqua reprehenderit aute qui voluptate dolor deserunt enim aute tempor ad dolor fugiat. Mollit aliquip elit aliqua eiusmod. Ex et anim non exercitation consequat elit dolore excepteur. Aliqua reprehenderit non culpa sit consequat cupidatat elit.', 'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 422077389352, 'submitter_id': 422077389352, 'assignee_id': 422077389352, 'organization_id': 361643882031, 'group_id': 4411436923156, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['amet', 'labore', 'voluptate'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 360003557971, 'brand_id': 360007086771, 'allow_channelback': False, 'allow_attachments': True}}


class MockResponse:
    def __init__(self):
        self.status_code = 200

    def json(self):
        return {'tickets': [{'url': 'https://zccsiddharth.zendesk.com/api/v2/tickets/1.json', 'id': 1, 'external_id': None, 'via': {'channel': 'sample_ticket', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2021-11-28T06:57:09Z', 'updated_at': '2021-11-28T06:57:10Z', 'type': 'incident', 'subject': 'Sample ticket: Meet the ticket', 'raw_subject': 'Sample ticket: Meet the ticket', 'description': 'Hi there,\n\nI’m sending an email because I’m having a problem setting up your new product. Can you help me troubleshoot?\n\nThanks,\n The Customer\n\n', 'priority': 'normal', 'status': 'open', 'recipient': None, 'requester_id': 422257406571, 'submitter_id': 422077389352, 'assignee_id': 422077389352, 'organization_id': None, 'group_id': 4411436923156, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['sample', 'support', 'zendesk'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 360003557971, 'brand_id': 360007086771, 'allow_channelback': False, 'allow_attachments': True, 'generated_timestamp': 1638082630}, {'url': 'https://zccsiddharth.zendesk.com/api/v2/tickets/2.json', 'id': 2, 'external_id': None, 'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2021-11-28T09:27:18Z', 'updated_at': '2021-11-28T09:27:18Z', 'type': None, 'subject': 'velit eiusmod reprehenderit officia cupidatat', 'raw_subject': 'velit eiusmod reprehenderit officia cupidatat', 'description': 'Aute ex sunt culpa ex ea esse sint cupidatat aliqua ex consequat sit reprehenderit. Velit labore proident quis culpa ad duis adipisicing laboris voluptate velit incididunt minim consequat nulla. Laboris adipisicing reprehenderit minim tempor officia ullamco occaecat ut laborum.\n\nAliquip velit adipisicing exercitation irure aliqua qui. Commodo eu laborum cillum nostrud eu. Mollit duis qui non ea deserunt est est et officia ut excepteur Lorem pariatur deserunt.', 'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 422077389352, 'submitter_id': 422077389352, 'assignee_id': 422077389352, 'organization_id': 361643882031, 'group_id': 4411436923156, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['est', 'incididunt', 'nisi'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 360003557971, 'brand_id': 360007086771, 'allow_channelback': False, 'allow_attachments': True, 'generated_timestamp': 1638091638}, {'url': 'https://zccsiddharth.zendesk.com/api/v2/tickets/3.json', 'id': 3, 'external_id': None, 'via': {'channel': 'api', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2021-11-28T09:27:18Z', 'updated_at': '2021-11-28T09:27:18Z', 'type': None, 'subject': 'excepteur laborum ex occaecat Lorem', 'raw_subject': 'excepteur laborum ex occaecat Lorem', 'description': 'Exercitation amet in laborum minim. Nulla et veniam laboris dolore fugiat aliqua et sit mollit. Dolor proident nulla mollit culpa in officia pariatur officia magna eu commodo duis.\n\nAliqua reprehenderit aute qui voluptate dolor deserunt enim aute tempor ad dolor fugiat. Mollit aliquip elit aliqua eiusmod. Ex et anim non exercitation consequat elit dolore excepteur. Aliqua reprehenderit non culpa sit consequat cupidatat elit.', 'priority': None, 'status': 'open', 'recipient': None, 'requester_id': 422077389352, 'submitter_id': 422077389352, 'assignee_id': 422077389352, 'organization_id': 361643882031, 'group_id': 4411436923156, 'collaborator_ids': [], 'follower_ids': [], 'email_cc_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['amet', 'labore', 'voluptate'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'followup_ids': [], 'ticket_form_id': 360003557971, 'brand_id': 360007086771, 'allow_channelback': False, 'allow_attachments': True, 'generated_timestamp': 1638091638}]}

class CustomConfig(configparser.ConfigParser):
    def __getitem__(self, key):
        if key == 'DEFAULT':
            return {'all_tickets_url': 'url',
                    'single_ticket_url': 'url',
                    'api_url': 'url',
                    'api_token': 'token',
                    'email_id': 'email',
                    }
        else:
            raise KeyError(str(key))



class TicketsTestCase(TestCase):
    def setUp(self):
        for ticket in Ticket.objects.all():
            ticket.objects.get(id=ticket.id).delete()

    @patch("requests.get", return_value=MockResponse())
    @patch('configparser.ConfigParser', side_effect=CustomConfig)
    def test_get_all_tickets(self, mock_response, config_parser):
        getAllTickets(None)
        self.assertEquals(len(Ticket.objects.all()), 3)
        self.assertIsNotNone(Ticket.objects.get(id=1))
        self.assertEquals(Ticket.objects.get(id=1).assignee_id, 422077389352)
        self.assertEquals(Ticket.objects.get(id=2).assignee_id, 422077389352)

    @patch("requests.get", return_value=MockIndividualTicket())
    @patch('configparser.ConfigParser', side_effect=CustomConfig)
    def test_get_individual_ticket_success(self, mock_response, config_parser):
        testTicket = detail(None,3)
        print(testTicket.json())
        self.assertIsNotNone(testTicket)
        self.assertEquals(testTicket.json()['ticket']['assignee_id'], 422077389352)
