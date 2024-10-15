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
    class Gender(models.Choices):
        M = "ผู้ชาย"
        F = "ผู้หญิง"
        LGBTQ = "LGBTQ+"
        O = "อื่นๆ"
    
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=10, null=True, unique=True)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    image_profile = models.ImageField(upload_to='profile_pic/',null=True,blank=True)
    
    def get_full_name(self):
        
        return f"{self.user.first_name} {self.user.last_name}"


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=255, null=True)
    available_time = models.DateTimeField()
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "ตรวจสอบ", "ตรวจสอบ"
        CANCELLED = "ยกเลิก", "ยกเลิก"
        COMPLETED = "จองสำเร็จ", "จองสำเร็จ"
    
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Linking with the built-in User model
    category = models.ForeignKey("Categories", on_delete=models.SET_NULL, null=True, blank=True)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    staff_id = models.ManyToManyField("Staff")
    service = models.ManyToManyField("Service")


class Service(models.Model):
    category = models.ForeignKey("Categories", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(max_length=255, null=True)
    def __str__(self):
        return self.name