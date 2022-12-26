from django.db import models
from django.contrib.auth.models import User

class Books(models.Model):
    upto_10_days =1
    upto_5_days =2
    upto_2_days =3
    TYPES = (
        (upto_10_days, 'up to 10 days'),
        (upto_5_days, 'up to 5 days'),
        (upto_2_days, 'up to 2 days'),
    )
    id = models.AutoField(db_column="id", primary_key=True)
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    year_published = models.IntegerField()    
    type = models.IntegerField(choices=TYPES) 

    def __str__(self):
        return self.name 

class Customers(models.Model):
    id = models.AutoField(db_column="id", primary_key=True)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    age = models.IntegerField()    

    def __str__(self):
        return self.name 

class Loans(models.Model):
    id = models.AutoField(db_column="id", primary_key=True)
    loan_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)
    customer = models.ForeignKey(Customers,related_name='loans',on_delete=models.CASCADE)
    book = models.ForeignKey(Books,related_name='loans',on_delete=models.CASCADE)

