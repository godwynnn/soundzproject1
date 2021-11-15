from django.db import models
from django.contrib.auth.models import User
from django.utils import tree
# Create your models here.

from .formatchecker import ContentTypeRestrictedFileField


class Customer(models.Model):
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE,unique=True)
    email=models.EmailField(null=True,blank=True)
    first_name=models.CharField(max_length=100,blank=True, null=True)
    second_name=models.CharField(max_length=100,blank=True, null=True)
    device = models.CharField(max_length=200, null=True, blank=True)
    date_joined=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user}'

    class Meta:
        ordering= ['-date_joined']


class Beat(models.Model):
    Genre=(
        ('Afro','Afro'),
        ('Afro-pop','Afro-pop'),
        ('Pop','Pop'),
        ('Hip-pop','Hip-pop'),
    )
    
    title=models.CharField(max_length=100,blank=True, null=True)
    price=models.IntegerField(null=True,blank=True,default=0)
    image=models.ImageField(upload_to='beat/image',null=True,blank=True, default='beat/image/stickers.jpg')
    slug=models.SlugField(null=True,blank=True)
    genre=models.CharField(max_length=100,blank=True,null=True, choices=Genre)
    sample=ContentTypeRestrictedFileField(upload_to='beat/sample_audio',blank=True,null=True,)
    full_beat=ContentTypeRestrictedFileField(upload_to='beat/full_audio',blank=True,null=True,)
    description=models.TextField(max_length=500,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering= ['-date_added']
    

class OrderBeat(models.Model):
    
    beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,null=True,blank=True,on_delete=models.SET_NULL)
    session=models.CharField(null=True,blank=True, max_length=200)
    is_ordered=models.BooleanField(default=False)
    date_added=models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer}'

    class Meta:
        ordering= ['-date_added']
    

class Order(models.Model):
    customer=models.ForeignKey(Customer,null=True,blank=True,on_delete=models.SET_NULL)
    session=models.CharField(null=True,blank=True, max_length=200)
    beats = models.ManyToManyField(OrderBeat,blank=True)
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(null=True,blank=True)


    def __str__(self):
        return f'{self.customer}'
    
    def get_total_price(self):
        amount=0
        for product in self.beats.all():
            amount+=product.beat.price
        return amount

    class Meta:
        ordering= ['-ordered_date']