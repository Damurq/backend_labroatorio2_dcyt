from django.db import models

# Create your models here.
class Program(models.Model):
    code = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, unique=True)
    number_semesters = models.SmallIntegerField(default=1)
    is_active = models.BooleanField(default = True)                                          
    def __str__(self):
        return self.name
    class Meta:  
        db_table = 'Program'

class Commission(models.Model):
    code = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, unique=True)
    description = models.CharField(max_length=1000, unique=True)
    is_active = models.BooleanField(default = True)                                            
    def __str__(self):
        return (self.name)
    class Meta:  
        db_table = 'Commission'

class Pensum(models.Model):
    code = models.AutoField(primary_key=True)
    description = models.CharField(max_length=1000, unique=True)
    program_code = models.ForeignKey(Program, on_delete= models.CASCADE)
    commission_code = models.ForeignKey(Commission, on_delete= models.CASCADE)#esto lo agregueee
    file_pdf = models.FileField(upload_to= 'pensum', null = False)
    expiration_date = models.DateField(auto_now =False, auto_now_add=False, blank=True, null=True)
    date_issue = models.DateField(auto_now =False, auto_now_add=True)
    is_active = models.BooleanField(default = True)                                            
    def __str__(self):
        return str(self.code)
    class Meta:  
        db_table = 'Pensum'