from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

            
        if len(postData['f_name']) < 2:
            errors['f_name'] = "First name must be at least 2 characters"


        if len(postData['l_name']) < 2:
            errors['l_name'] = "Last name must be at least  characters"


        if len(postData['email']) < 1:
            errors['email'] = "Email cannot be empty you suck"
        if not EMAIL_REGEX.match(postData['email']):   
            errors['email'] = "Invalid email address you suck"
        

        if len(postData['pw']) < 8:
            errors['pw_len'] = "Password should be at least 8 characters"
        if postData['pw'] != postData['confirm_pw']:
            errors['con_pw'] = "Password confirmation must match the password"


        return errors

    def login_validator(self, postData):
        errors = {}
        email = postData['email']
        pw = postData['pw']
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


        date = User.objects.filter(email = email)

        if len(email) < 1:
            errors['email'] = "Email cannot be empty you suck"
        elif not EMAIL_REGEX.match(postData['email']):   
            errors['email'] = "Invalid email address you suck"

        if len(pw) < 8:
            errors['pw'] = "Password should be at least 8 characters you suck"



        return errors


class TripManager(models.Manager):
    def trip_validator(self,postData):
        errors = {}
        destination = postData['destination']
        plan = postData['plan']
        start_date = postData['start_date']
        end_date = postData['end_date']

        if len(destination) < 3:
            errors['destination'] = "Destination must be at least 3 you suck"
        
        if len(plan) < 3:
            errors['plan'] = "Plan must be at least 3 characters you suck"

        if start_date == "":
            errors['start_date'] = "You must enter valid start date"

        if end_date == "":
            errors['end_date'] = "You must enter valid end date"

        return errors


class User(models.Model):
    f_name = models.CharField(max_length=30)
    l_name = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    pw = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateField(auto_now_add=True, blank=True, null=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()
    user = models.ForeignKey(User, related_name='trips', on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateField(auto_now_add=True, blank=True, null=True)
    objects = UserManager()
    objects = TripManager()

