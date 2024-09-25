from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class City(models.Model):
    city_id = models.IntegerField(primary_key=True)
    city_name = models.CharField(max_length=50)
    state_name = models.CharField(max_length=50)
    def __str__(self):
        return  str(self.city_name)

class Location(models.Model):
    loc_id = models.IntegerField(primary_key=True)
    loc_name = models.CharField(max_length=50)
    city_id = models.ForeignKey(City,on_delete=models.CASCADE)
    def __str__(self):
        return  str(self.loc_id)

class House(models.Model):
    house_id = models.CharField(max_length=12,primary_key=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    address = models.TextField()
    area = models.FloatField()
    bhk = models.IntegerField()
    description = models.TextField()
    sold = models.BooleanField()
    img1 = models.ImageField(upload_to='house_images/')
    img2 = models.ImageField(upload_to='house_images/')
    img3 = models.ImageField(upload_to='house_images/')
    cctv = models.BooleanField()
    children_play_area = models.BooleanField()
    landscape = models.BooleanField()
    garage = models.BooleanField()
    power_backup = models.BooleanField()
    lifts = models.BooleanField()
    cycling_jogging = models.BooleanField()
    fire_fighting = models.BooleanField()
    temple = models.BooleanField()
    
    def __str__(self):
        return  self.house_id

class Dealer(models.Model):
    dealer_id = models.CharField(max_length=10,primary_key=True)
    dealer_name = models.CharField(max_length=50)
    house_id = models.ForeignKey(House,on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=10)
    email_id = models.EmailField(max_length=254)
    address = models.TextField()
    def __str__(self):
        return  self.dealer_id+" , "+self.house_id.house_id

class Customer(models.Model):
    customer_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=10)
    email = models.EmailField()
    def __str__(self):
        return  self.customer_name


class Housesold(models.Model):
    house_id = models.CharField(max_length=12,primary_key=True)
    date_of_deal = models.DateField()
    customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
    def __str__(self):
        return self.house_id

class Customercontacted(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()
    msg = models.TextField()
    def __str__(self):
        return self.first_name+ " " +self.last_name
    

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username}"

    class Meta:
        ordering = ('timestamp',)