from django.db import models

# Create your models here.
class Users(models.Model):     
    first_name = models.CharField(max_length=155, null=True)
    last_name = models.CharField(max_length=155, null=True)
    birth_date = models.DateField()
    email = models.EmailField(null=True)
    username = models.CharField(max_length=15,null=True)
    password = models.CharField(max_length=255)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"