from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

# Extended User Model
class ExtendUser(models.Model):
    id = models.UUIDField(primary_key = True, editable = False, default = uuid.uuid4)
    id_user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True)
    phone_code = models.CharField(max_length = 100, null = True)


    def __str__(self):
        return self.phone_number
    
class AdminKey(models.Model):
    id = models.UUIDField(primary_key = True, editable = False, default = uuid.uuid4)
    key = models.CharField(max_length = 100, blank = True)


