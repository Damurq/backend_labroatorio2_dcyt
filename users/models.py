from django.db import models

# Create your models here.
from pensum.models import *
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.
class Employee(models.Model):
    """Modelo Employee"""
    ROLE = (
        ("A","Admin"),
        ("G","Gestor de programas")
    )
    code = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    program_code = models.ForeignKey(Program, on_delete=models.CASCADE, default = 0)
    role = models.CharField(max_length=2,choices=ROLE,default="G")
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    photo = models.ImageField(
        upload_to='pictures',
        default='pictures/default.png',
        max_length=255
    )
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name +" "+ self.last_name

    class Meta:  # pylint: disable=too-few-public-methods
        """Propiedades adicionales del modelo Employee"""
        db_table = 'Employee'