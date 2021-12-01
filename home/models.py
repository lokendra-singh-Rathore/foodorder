from math import pi
from django.db import models
import string
import random
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.fields import AutoField
from django.db.models.signals import post_save
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json


from django.db.models.fields.related import ForeignKey

class pizza(models.Model):
    name=models.CharField(max_length=100,null=True)
    price=models.IntegerField(default=100)
    image=models.CharField(max_length=1000)

    def __str__(self):
        return self.name



def rendom_string_genrator(size=10,chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

CHOICES =(
    ("Order Recived" ,"Order Recived"),
    ("Baking","Baking"),
    ("Baked","Baked"),
    ("Out for Delivery","Out for Delivery"),
    ("Deliverd","Deliverd")

)

class Order(models.Model):
    pizza=models.ForeignKey(pizza, on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    order_id=models.CharField(max_length=100,blank=True)
    amount=models.IntegerField(default=100)
    status=models.CharField(choices=CHOICES, default="Order Recived",max_length=100)
    date=models.DateTimeField(auto_now_add=True)

    def save(self, *args,**kwargs):
        if not len(self.order_id):
            self.order_id=rendom_string_genrator()
        super(Order,self).save(*args,**kwargs)

    def __str__(self):
        return self.order_id


    @staticmethod
    def give_order_detail(order_id):
        instance=Order.objects.filter(order_id=order_id).first()
        data={}
        data['order_id']=instance.order_id
        data['amount']=instance.amount
        data['status']=instance.status

        progress_percentage=0
        if instance.status=='Order Recived':
            progress_percentage=20

        elif instance.status=='Baking':
            progress_percentage=40

        elif instance.status=='Baked':
            progress_percentage=60

        elif instance.status=='Out for Delivery':
            progress_percentage=80

        elif instance.status=='Deliverd':
            progress_percentage=100

        data['progress'] = progress_percentage

        return data

    
@receiver(post_save, sender=Order)
def order_status_handler(sender, instance,created , **kwargs):
    
    if not created:
        print("###################")
        channel_layer = get_channel_layer()
        data  = {}
        data['order_id'] = instance.order_id
        data['amount'] = instance.amount
        data['status'] = instance.status
        data['date'] = str(instance.date)
        progress_percentage = 20
        if instance.status == 'Order Recieved':
            progress_percentage = 20
        elif instance.status == 'Baking':
            progress_percentage = 40
        elif instance.status == 'Baked':
            progress_percentage = 60
        elif instance.status == 'Out for delivery':
            progress_percentage = 80
        elif instance.status == 'Order recieved':
            progress_percentage = 100
    
        
        data['progress'] = progress_percentage
        async_to_sync(channel_layer.group_send)(
            'order_%s' % instance.order_id,{
                'type': 'order_status',
                'value': json.dumps(data)
            }
        )