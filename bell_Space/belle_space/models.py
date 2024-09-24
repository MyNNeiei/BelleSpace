from django.db import models
from django.contrib.auth.models import User 
# Create your models here.
# class Users(models.Model):     
#     first_name = models.CharField(max_length=155, null=True)
#     last_name = models.CharField(max_length=155, null=True)
#     birth_date = models.DateTimeField()
#     email = models.EmailField(null=True)
#     username = models.CharField(max_length=15,null=True)
#     password = models.CharField(max_length=255)
#     
#     def get_full_name(self):
#         return f"{self.first_name} {self.last_name}"
class UsersDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=10, null=True)

    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=255, null=True)
    available_time = models.DateField()


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "Pending", "Pending"
        CANCELLED = "Cancelled", "Cancelled"
        COMPLETED = "Completed", "Completed"
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Linking with the built-in User model
    service = models.ForeignKey("Service", on_delete=models.SET_NULL, null=True, blank=True)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    staff = models.ManyToManyField("Staff")


class Service(models.Model):
    category = models.ForeignKey("Categories", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)


class Categories(models.Model):
    name = models.CharField(max_length=255, null=True)



    