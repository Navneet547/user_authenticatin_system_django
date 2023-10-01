from django.shortcuts import render,redirect
from django.views import *
from app1.models import *
from django.core.mail import send_mail
import random

# Create your views here.
class login_view(View):
    def get(self,request):
       
        return render(request,"login.html")
    def post(self, request):
     input_username2 = request.POST.get('username')
     input_password2 = request.POST.get('password')
    
     try:
        user = usermodel.objects.get(username=input_username2)
        
        if input_password2 == user.password:
            return render(request, 'home.html')
        else:
            return render(request, 'login.html', {"alertpassword": "**wrong password**"})
            
     except usermodel.DoesNotExist:
          return render(request, 'login.html', {"alertemail": "**wrong email id**"})

   
 

class signup_view(View):
    def get(self,request):

        return render(request,"signup.html")

    def post(self,request):
        input_username=request.POST.get('username')
        input_email=request.POST.get('email')
        input_password=request.POST.get('password')
        input_cpassword=request.POST.get('cpassword')
        alert="**miss match password**"

        if(input_cpassword==input_password):
            usermodel(username=input_username,useremail=input_email,password=input_password).save()
            return  render(request,'login.html')
        else:
            return render(request,'signup.html',{'alert':alert})


class forgot_view(View):
    def get(self,request):

        return render(request,"forgot.html")
    def post(self,request):
        f_email=request.POST.get('email')
        otp=random.randint(1000,9999)
       
        try:
            for_email= usermodel.objects.get(useremail=f_email)
            
            send_mail(
            "OTP Verification",
            f'here is your otp:{otp}',
            "navneet.kumar@indicchain.com",
            [f'{f_email}'],
            fail_silently=False,
            )
            # return render(request, 'otp.html')
            request.session['otp'] = otp 
            return redirect('otp')
       
        except usermodel.DoesNotExist:
            return render(request, 'forgot.html', {"alertemail": "**wrong email id**"})

class otp_view(forgot_view) :
    def get(self,request):
        return render(request,"otp.html")
    def post(self,request):
        input_otp=request.POST.get('otp')
        otp = request.session.get('otp') 
        if(input_otp==str(otp)):
            # return render(request,'reset.html')
            return render(request,'reset.html')
        
        return render(request,'otp.html',{'otp_alert':'**wrong otp**'})


class reset_view(View):
    def get(self,request):
        return render(request,"reset.html")