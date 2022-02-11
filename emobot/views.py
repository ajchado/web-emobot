from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
# from sqlalchemy import null
from .forms import *
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import PersonForm
import re
import hashlib
from .models import Person, SessionTable, EmotionTable
from bootstrap_modal_forms.forms import BSModalModelForm
from webEmobot.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
import csv

# Create your views here.
class homeView(View):
    def get(self, request):
        users = Person.objects.all()
        for user in users:
            if(user.isLoggedIn == True):
                return render(request, 'home.html', {'user': user})

        return redirect('emobot:login')

class dashboardView(View):
    def get(self, request):
        users = Person.objects.all()
        emotions = EmotionTable.objects.all()
        context = { 
            'emotions': emotions,
        }
        for user in users:
            if(user.isLoggedIn == True):
                return render(request, 'dashboard.html', context)   
                
        return redirect('emobot:login')

    def post(self, request):
        user = Person.objects.all()
        sessions = SessionTable.objects.all()
        emotions = EmotionTable.objects.all()
        mylist=zip(user, sessions,emotions)
        context = { 
            'mylist': mylist,
        } 
        if request.method == 'POST':
            if 'del123' in request.POST: 
                SessionTable.objects.all().delete()
                EmotionTable.objects.all().delete()
                messages.error(request, 'Data Successfully Deleted!', extra_tags = 'deleted123')
        return render(request, 'dashboard.html', context)  

class loginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        uname = request.POST.get('username')
        pwd = request.POST.get('password')  
      
      
        if Person.objects.filter(username=uname).count() != 0:
            account = Person.objects.get(username=uname)
            string=pwd
            encoded=string.encode()
            result = hashlib.sha256(encoded)
            passs = result.hexdigest()
            print(passs)
            if account.isDeleted == False:
                if account.password != passs:
                    messages.error(request, 'Incorrect Password!', extra_tags = 'login_incorrect_password')
                    return render(request, 'login.html')
                if account.isActivated == False:
                    messages.error(request, 'Check your email and activate your account', extra_tags = 'not_activated')
                    return render(request, 'login.html')           
                else:
                    Person.objects.filter(username=uname).update(isLoggedIn = True)
                    return redirect('emobot:home')
            else:
                messages.error(request, 'User Is Deleted!', extra_tags = 'deleted')
                return render(request, 'login.html')
        else:
            messages.error(request, 'Username Does Not Exist!', extra_tags = 'login_user_notexist')

        return render(request, 'login.html')

class logoutView(View):
    def get(self, request):
        users = Person.objects.all()
        for user in users:
            if(user.isLoggedIn == True):
                Person.objects.update(isLoggedIn = False)

        return redirect('emobot:login')

class registerView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        form = PersonForm(request.POST, request.FILES)
        fname = request.POST.get("firstName")
        lname = request.POST.get("lastName")
        email = request.POST.get("email")
        uname = request.POST.get("username")
        passw = request.POST.get("password")
        cpassw = request.POST.get("confirm_password")
        gndr = request.POST.get("gender")
      
#        if len(passw) < 8:
#            messages.error(request,'Make sure your password is at lest 8 letters', extra_tags = 'pass_long')
#            return redirect('emobot:register')
#        if re.search('[0-9]',passw) is None:
#            messages.error(request,'ake sure your password has a number in it', extra_tags = 'pass_num')
#            return redirect('emobot:register')
#        if re.search('[A-Z]',passw) is None: 
#            messages.error(request,'Make sure your password has a capital letter in it', extra_tags = 'pass_cap')
#            return redirect('emobot:register')
        if form.is_valid():
            if passw == cpassw:
            #    passw = bytes(passw,"ascii")
            #    passw = bcrypt.hashpw(passw, salt)
                if Person.objects.filter(username=uname).exists():
                    messages.error(request,'Username already taken', extra_tags = 'user_error')
                    return redirect('register.html')
                elif Person.objects.filter(email=email).exists():
                    messages.error(request, 'Email already used', extra_tags = 'user_error')
                    return redirect('register.html')
                else:
                    string=passw
                    encoded=string.encode()
                    result = hashlib.sha256(encoded)
                    passs = result.hexdigest()
                    print(passs)
                    sub = PersonForm(request.POST)
                    code = User.objects.make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
                    subject = 'EmoBot Activate Account' 
                    message = 'Activation Code: %s \nActivation Link: http://127.0.0.1:8000/emobot/activate/' %code
                    recepient = str(sub['email'].value())
                    send_mail(subject, 
                    message, EMAIL_HOST_USER, [recepient], fail_silently = False)
                    form = Person(firstName=fname, lastName=lname, email=email, username=uname, password=passs, gender=gndr, code=code)
                    form.save()
                    messages.success(request,'The user has been successfully registered!', extra_tags = 'successful')
                    return render(request, 'register.html')
            else:
                messages.error(request, 'Password does not match!', extra_tags = 'password_error')
                return render(request, 'register.html')
            
        else:
            messages.error(request, 'Register unsuccessful', extra_tags = 'password_error')
            return redirect('emobot:register')

class userView(View):
    def get(self, request):
        user = Person.objects.get(isLoggedIn=True)
        emotions = EmotionTable.objects.filter(userID = user.personID)
        context = { 
            'emotions': emotions,
            'user': user,
        }    
        if(user.isLoggedIn == True):
            return render(request, 'user.html', context)
                
        return redirect('emobot:login')

class accountsettingsView(View):
    def get(self, request):
        users = Person.objects.all()
        user = Person.objects.get(isLoggedIn=True)
        print(user.username)
        for user in users:
            if(user.isLoggedIn == True):
                return render(request, 'account-settings.html', {'user': user})
                
        return redirect('emobot:login')

    def post(self, request):
        if request.method == 'POST':
            if 'save' in request.POST: 
                username = request.POST.get('username')
                email = request.POST.get('email')
                gender = request.POST.get('gender')
                if Person.objects.filter(username=username).exists():
                    messages.error(request, 'Username already taken!', extra_tags = 'email_exist')
                    return redirect('emobot:account-settings')                
                if Person.objects.filter(email=email).exists():
                    messages.error(request, 'Email already used!', extra_tags = 'email_exist')
                    return redirect('emobot:account-settings')
                if Person.objects.filter(isLoggedIn = True):
                    Person.objects.filter(isLoggedIn = True).update(username=username, email=email, gender=gender)
                    messages.error(request, 'Successfully Updated Account Settings!', extra_tags = 'updated')
                    return redirect('emobot:account-settings')                
        return redirect('emobot:account-settings')

class changepasswordView(View):
    def get(self, request):
        users = Person.objects.all()
        user = Person.objects.get(isLoggedIn=True)
        print(user.username)
        for user in users:
            if(user.isLoggedIn == True):
                return render(request, 'change-password.html', {'user': user})
                
        return redirect('emobot:login')

    def post(self, request):
        if 'save' in request.POST: 
            oldpass = request.POST.get('oldpass')
            newpass = request.POST.get('newpass')
            confirm = request.POST.get('confirm')
            string=oldpass
            encoded=string.encode()
            result = hashlib.sha256(encoded)
            passs = result.hexdigest() 

            if Person.objects.filter(isLoggedIn = True) and Person.objects.filter(password = passs).exists():
                if newpass != confirm:
                    messages.error(request, 'New Password Does Not Match!', extra_tags = 'password_notmatch')
                else: 
                    string=newpass
                    encoded=string.encode()
                    result = hashlib.sha256(encoded)
                    newpass = result.hexdigest() 
                    Person.objects.filter(password = passs).update(password=newpass)
                    messages.error(request, 'Password Updated!', extra_tags = 'password_updated')    
            else:
                messages.error(request, 'Invalid Old Password!', extra_tags = 'password_invalid')

        return render(request, 'change-password.html')

class publicprofileView(View):
    def get(self, request):
        users = Person.objects.all()
        user = Person.objects.get(isLoggedIn=True)
        print(user.username)
        for user in users:
            if(user.isLoggedIn == True):
                return render(request, 'public-profile.html', {'user': user})
                
        return redirect('emobot:login')

    def post(self, request):
        if request.method == 'POST':
            if 'save1' in request.POST: 
                firstName = request.POST.get('firstName')
                lastName = request.POST.get('lastName')
                shortbio = request.POST.get('bio')
                image = request.FILES['image']
                if Person.objects.filter(isLoggedIn = True):
                    Person.objects.filter(isLoggedIn = True).update(firstName=firstName, lastName=lastName, shortbio=shortbio, image=image)
                messages.error(request, 'Public Profile Successfully Updated!', extra_tags = 'updated_p')
        return render(request, 'public-profile.html')

class deleteaccountsView(View):
    def get(self, request):
        users = Person.objects.all()
        user = Person.objects.get(isLoggedIn=True)
        print(user.username)
        for user in users:
            if(user.isLoggedIn == True):               
                return render(request, 'delete-account.html', {'user': user})
                
        return redirect('emobot:login')

    def post(self, request):
        if request.method == 'POST':
            if 'del' in request.POST: 
                if Person.objects.filter(isLoggedIn = True).exists():
                    Person.objects.filter(isLoggedIn = True).update(isDeleted ="1", isLoggedIn = "0", isActivated = "0")
                    messages.error(request, 'Profile Successfully Deleted!', extra_tags = 'deleted')
        return redirect('emobot:login')

class termsandconditionsView(View):
    def get(self, request):

        return render(request, 'terms-and-conditions.html')
    def post(self, request):

         return redirect('emobot:register')

class forgotpassowrdView(View):
    def get(self, request):
        
        return render(request,'forgot-password.html')
    def post(self, request):
        if request.method == 'POST':
            email = request.POST.get('email')
            if 'reset' in request.POST and Person.objects.filter(email = email).exists() :
                password = User.objects.make_random_password(length=6, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
                print(password)
                sub = PersonForm(request.POST)
                subject = 'EmoBot Reset Password' 
                message = 'Your new password is %s' %password
                string=password
                encoded=string.encode()
                result = hashlib.sha256(encoded)
                passs = result.hexdigest()
                Person.objects.filter(email = email).update(password=passs)
                recepient = str(sub['email'].value())
                send_mail(subject, 
                message, EMAIL_HOST_USER, [recepient], fail_silently = False)
                messages.error(request, 'A new password has been sent to your email', extra_tags = 'password_sent')
            else:
                messages.error(request, 'Email not registered', extra_tags = 'email_not_found')
                return redirect('emobot:forgot-password')

        return redirect('emobot:forgot-password')

class activateView(View):
    def get(self, request):

        return render(request, 'activate.html')
    def post(self, request):
        code = request.POST.get('code')
        if request.method == 'POST':
            if 'activate' in request.POST and Person.objects.filter(code = code).exists():
                Person.objects.filter(code = code).update(isActivated ="1")
                messages.error(request, 'Account successfully activated', extra_tags = 'activated')
                return redirect('emobot:activate')
            else:
                messages.error(request, 'Invalid activation code', extra_tags = 'invalid_code')
                return redirect('emobot:activate')

        return redirect('emobot:activate')


def export_csv1(request):
    user = Person.objects.get(isLoggedIn=True)
    emotions = EmotionTable.objects.filter(userID = user.personID)
    context = { 
        'emotions': emotions,
    }  
    response=HttpResponse(content_type='text/csv')
    response['content-disposition'] = 'attachment; filename=%s.csv' %user.username
    
    writer=csv.writer(response)
    writer.writerow(['SessionID','Question_Answered','Emotion','Duration','Date',])
    

    for emotion in emotions:
        writer.writerow([emotion.SessionID_id,emotion.SessionID.Question_Answered,emotion.Emotion,emotion.SessionID.Duration,emotion.SessionID.Date,])

    return response

def export_csv2(request):
    emotions = EmotionTable.objects.all()
    context = { 
        'emotions': emotions,
    } 

    response=HttpResponse(content_type='text/csv')
    response['content-disposition'] = 'attachment;filename=emobot.csv' 
    
    writer=csv.writer(response)
    writer.writerow(['Username','SessionID','Question_Answered','Emotion','Duration','Date',])
    
    for emotion in emotions:
        
        writer.writerow([emotion.userID.username, emotion.SessionID_id, emotion.SessionID.Question_Answered, emotion.Emotion, emotion.SessionID.Duration, emotion.SessionID.Date])

    return response    