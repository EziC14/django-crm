from django.db import models
from crequest.middleware import CrequestMiddleware
from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid

def get_user():
    current_request = CrequestMiddleware.get_request()
    result = None
    if current_request is not None:
        result = None if not current_request.user.is_authenticated else current_request.user

class Updater(models.Model):
    is_active  = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de creación",null=True, blank=True,)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización",null=True, blank=True,)
    created_by = models.CharField(max_length=500, null=True, blank=True, default=None, verbose_name="Creado por")
    updated_by = models.CharField(max_length=500, null=True, blank=True, default=None, verbose_name="Actualizado por")
    deleted_at = models.DateTimeField(null=True, blank=True, default=None, verbose_name="Fecha de eliminación")
    deleted_by = models.CharField(max_length=500, null=True, blank=True, default=None, verbose_name="Eliminado por")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_user()
        if user is not None:
            if not hasattr( self, 'created_by') or  self.created_by is None:
                self.created_by = user.username
            self.updated_by = user.username
        super(Updater, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        user = get_user()
        if user is not None:
            self.deleted_by = user.username
            self.deleted_at = timezone.now()
            self.save()
        else:
            super(Updater, self).delete(*args, **kwargs)

class Company(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Customer(Updater):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='customers')
    sales_rep = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='customers')
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Interaction(Updater):
    TYPE_CHOICES = [
        ('Phone', 'Phone'),
        ('Email', 'Email'),
        ('SMS', 'SMS'),
        ('Facebook', 'Facebook'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='interactions')
    sales_rep = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    interaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    timestamp = models.DateTimeField()
    notes = models.TextField(blank=True)

    class Meta:
        indexes = [models.Index(fields=['timestamp']), models.Index(fields=['interaction_type'])]

    def __str__(self):
        return f"{self.get_interaction_type_display()} with {self.customer} on {self.timestamp}"
