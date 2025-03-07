from django.db import models

# Create your models here.
class Logindata(models.Model):
    userid=models.CharField(max_length=100,primary_key=True)
    password=models.CharField(max_length=100)
    usertype=models.CharField(max_length=100)
    def __str__(self):
        return self.userid


class admindata(models.Model):
    email = models.CharField(max_length=100, primary_key=True)
    name= models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class medicaldata(models.Model):
    email=models.CharField(max_length=100,primary_key=True)
    store_name = models.CharField(max_length=100)
    owner= models.CharField(max_length=100)
    lno= models.CharField(max_length=100)
    address= models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    def __str__(self):
        return self.store_name

class medicinedata(models.Model):
    med_id=models.AutoField(primary_key=True)
    med_name=models.CharField(max_length=100)
    lno=models.CharField(max_length=100)
    company=models.CharField(max_length=100)
    med_type=models.CharField(max_length=100)
    unit_price=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    email_of_medical=models.CharField(max_length=100)
    def __str__(self):
        return "%s %s" % (self.med_name,self.med_id)
