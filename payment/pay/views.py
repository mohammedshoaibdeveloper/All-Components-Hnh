from django.shortcuts import render,HttpResponse

from django.conf import settings # new
from django.http.response import JsonResponse # new
from django.views.decorators.csrf import csrf_exempt # new
from django.views.generic.base import TemplateView
import stripe


#secrete key
stripe.api_key='sk_test_SD1VLYLcME6RYimXA3xxNKXW00eXfNnzuC'

# Create your views here.

def home(request):
    
    return render(request,'home.html')


def checkout(request):
    if request.method=="POST":
       
        
        charge = stripe.Charge.create(
        amount=100,
        currency='usd',
        description='A Django charge',
        source=request.POST['stripeToken']
        )
        if(charge['paid']==True):
            return HttpResponse('paid')
        else:
            return HttpResponse('Fail')

            
            
            
        
       
        
    



