from django.db import models


# Create your models here.
class Ticket(models.Model):
    def __str__(self):
        return str(self.id)+" "+str(self.created_at)+" "+str(self.requester_id)

    assignee_id = models.IntegerField(max_length=200)
    created_at = models.TimeField()
    description = models.CharField(null=True, max_length=200)
    due_at = models.DateTimeField(null=True)
    external_id = models.CharField(null=True, max_length=200)
    group_id = models.IntegerField(null=True, max_length=200)
    has_incidents = models.BooleanField(null=True, )
    id = models.IntegerField(primary_key=True)
    organization_id = models.IntegerField(null=True, max_length=200)
    priority = models.CharField(null=True, max_length=200)
    problem_id = models.IntegerField(null=True, max_length=200)
    raw_subject = models.CharField(null=True, max_length=200)
    recipient = models.EmailField(null=True)
    requester_id = models.IntegerField(null=True, max_length=200)
    status = models.CharField(null=True, max_length=200)
    subject = models.CharField(null=True, max_length=200)
    submitter_id = models.IntegerField(null=True, max_length=200)
    type = models.CharField(null=True, max_length=200)
    updated_at = models.DateTimeField(null=True)
    url = models.URLField(null=True)

