from django.db import models
from django.contrib.auth.models import User


ROLE_CHOICES = (
    ('Requester', 'Requester'),
    ('Scribe', 'Scribe'),
)

REQUEST_STATUS = (
    ('Open', 'Open'),
    ('Filled', 'Filled'),
    ('Completed', 'Completed'),
)

APPLICATION_STATUS = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Rejected', 'Rejected'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    academic_level = models.CharField(max_length=20)
    institution = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}"

class ExamRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    university = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    module_name = models.CharField(max_length=100)
    exam_date = models.DateTimeField()
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=REQUEST_STATUS, default='Open')

    def __str__(self):
        return f"{self.module_name} ({self.university})"

class Application(models.Model):
    scribe = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    exam_request = models.ForeignKey(ExamRequest, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=APPLICATION_STATUS, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # scribe can only apply once to a specific exam
        unique_together = ('scribe', 'exam_request')

    def __str__(self):
        return f"{self.scribe.username} applied for {self.exam_request.module_name}"