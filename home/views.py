from django.contrib.auth.models import AnonymousUser, User
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
import json
from django.views.decorators.csrf import csrf_exempt

from . models import pizza,Order

def index(request):
    pizzas=pizza.objects.all()
    orders=Order.objects.all()
    context={'pizzas':pizzas,'orders':orders}
    return render(request,'index.html',context)


def order_status(request,order_id):
    order=Order.objects.filter(order_id=order_id).first()
    if order is None:
        return redirect('index')
    context={'order':order}
    return render(request,'order_status.html',context)

@csrf_exempt
def order_pizza(request):
    user=request.user
    data=json.loads(request.body)
    print(data)
    try:
        pizz=pizza.objects.get(id=data.get('id'))
        order=Order(user=user, pizza=pizz,amount=pizz.price)
        order.save()
        
        return JsonResponse({'msg':'order Created','status':True})
    except pizza.DoesNotExist:
        return JsonResponse({'error':'somthing went Wrong','status':False})
