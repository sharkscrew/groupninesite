from django.db import models

# Create your models here.
class Genders(models.Model):
    class Meta:
        db_table = 'tbl_genders'

    gender_id = models.BigAutoField(primary_key=True, blank=False)
    gender = models.CharField(max_length=55, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.gender

class Users(models.Model):
    class Meta:
        db_table = 'tbl_users'

    user_id = models.BigAutoField(primary_key=True, blank=False)
    full_name = models.CharField(max_length=55, blank=False)
    gender = models.ForeignKey(Genders, on_delete=models.CASCADE)
    birthdate = models.DateField(blank=False)
    address = models.CharField(max_length=255, blank=False)
    contact_numbers = models.CharField(max_length=55, blank=False)
    email = models.EmailField(max_length=55, blank=True, unique=True) 
    username = models.CharField(max_length=55, blank=False, unique=True)
    password = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

