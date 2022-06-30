from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# Abstractuser does not allow me to modify the attributes 

class Assistant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    team = models.CharField(max_length=200, null=True, choices=[("DZ", "DZ"), ("FR", "FR")])
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(verbose_name ='email', max_length=60, unique=True)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="date joined")

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.user.username 


def get_file_path (self, filename):
    return f'media/{self.pk}/{str(filename)}'


class Ticket (models.Model):
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='assistant_FR_user')
    assigned_to = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='assistant_DZ_user')
    
    STATUS = (
        ("Pending", "PENDING",),
        ("Assigned", "ASSIGNED"),
        ("Completed", "COMPLETED"),
    )

    status = models.CharField(max_length=200, null=True, choices=STATUS, default="Pending")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    contextual_info = models.TextField(blank=True)
    deadline = models.DateField(blank=False, null=False)
    created_on = models.DateField(auto_now_add=True)

    files = models.FileField(blank=True, upload_to='media', null=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title