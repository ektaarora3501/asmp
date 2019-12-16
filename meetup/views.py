from django.shortcuts import render,redirect
from meetup.models import Register_user,Notice,Event
from meetup.forms import RegisterForm,LoginForm,UpdateForm,SetNoticeForm,SetEventForm
from django.http import HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.conf import settings
import datetime
# from hashing import *
# from django.core.mail import EmailMessage


# for home page
def index(request):
    return render(request,'home.html')

# registeration form
def Register(request):
    if request.method=='POST':
       form =RegisterForm(request.POST)
       print("post")

       if form.is_valid():
           user=form.cleaned_data['first_name']
           print(user)
           us=Register_user()
           #url=confirm/user
           print("form valid")
           us.first_name=form.cleaned_data['first_name']
           name=form.cleaned_data['first_name']
           us.last_name=form.cleaned_data['last_name']
           us.email=form.cleaned_data['email']
           us.branch=form.cleaned_data['choice']
           us.curr_year=form.cleaned_data['curr_year']
           us.roll_no=form.cleaned_data['adm_no']
           user=form.cleaned_data['password']
           # us.password=hash_password(user)                     #done by me
           print(us.password)
           us.save()
           print("branch,curr_year",us.branch,us.curr_year)

           return HttpResponseRedirect(reverse('login_user'))

    else:
        form=RegisterForm() # in case method is get simply display the form
    context={
    'form':form,
    }


    return render(request,'Register.html',context)

def login(request):
   if request.session.get('name'):
       nm=request.session.get('name')
       return HttpResponseRedirect(reverse('user-dashboard',args=(nm,)))
   else:

        if request.method=='POST':
            form =LoginForm(request.POST)
            print("post")

            if form.is_valid():
                 print("form valid")
                 user=form.cleaned_data['adm_no']
                 request.session['name']=user
                 print(request.session['name'])
                 print("sesssion set!")
                 return HttpResponseRedirect(reverse('user-dashboard',args=(user,)))

        else:
             print('here')
             form=LoginForm()
        context={
         'form':form,
         }

        return render(request,'login.html',context)


def dashboard(request,user):
    if request.session.get('name')==user:
        us=Register_user.objects.get(roll_no=user)
        if request.method == 'POST' :
            #if request.POST['msg']:
            #       print(request.POST['msg'])
            if request.FILES['myfile']:
                myfile = request.FILES['myfile']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
                us.img_link=uploaded_file_url
                us.save()
                #my = request.POST['msg']
                #print(my)
                print(uploaded_file_url)
                return render(request, 'dashboard.html', {
                    'us':us,'user':user,
                    })

        return render(request,'dashboard.html',{'user':user,'us':us})



    else:
        return HttpResponseRedirect(reverse('login_user'))


def logout(request,user):
    try:
        del request.session['name']
        print("user deleted")
        print(request.session['name'])
    except :
          pass
    return HttpResponseRedirect(reverse('login_user'))

def profile(request,user):
    if request.session.get('name'):
        us=Register_user.objects.get(roll_no=user)

        if request.method=='POST':
            form =UpdateForm(request.POST)
            print("post")

            if form.is_valid():
                print("form valid")
                us.github=form.cleaned_data['github_link']
                us.email=form.cleaned_data['email']
                us.skill1=form.cleaned_data['skill1']
                us.skill2=form.cleaned_data['skill2']
                us.skill3=form.cleaned_data['skill3']
                us.skill4=form.cleaned_data['skill4']
                us.ntech1=form.cleaned_data['ntech1']
                us.ntech2=form.cleaned_data['ntech2']
                us.ntech3=form.cleaned_data['ntech3']
                us.ntech4=form.cleaned_data['ntech4']
                us.summary=form.cleaned_data['summary']
                us.save()
                return HttpResponseRedirect(reverse('user-dashboard',args=(user,)))

        else:
                print(us.first_name)
                form=UpdateForm(initial={'email':us.email,'github_link':us.github,'summary':us.summary})
        context={
        'name':us.first_name,
        'branch':us.branch,
        'form':form,
        }
        return render(request,'profile.html',context=context)

    else:
        return HttpResponseRedirect(reverse('login_user'))



def get_skill_tech(request,skill):
    if request.session.get('name'):
        us1=Register_user.objects.filter(skill1=skill).all()
        us2=Register_user.objects.filter(skill2=skill).all()
        us3=Register_user.objects.filter(skill3=skill).all()
        us4=Register_user.objects.filter(skill4=skill).all()
        context={
        'us1':us1,
        'us2':us2,
        'us3':us3,
        'us4':us4,
        'skill':skill,
        }
        return render(request,'skill_tech.html',context=context)
    else:
        return HttpResponseRedirect(reverse('login_user'))

def get_member(request,group):
    if request.session.get('name'):
        us1=Register_user.objects.filter(ntech1=group).all()
        us2=Register_user.objects.filter(ntech2=group).all()
        us3=Register_user.objects.filter(ntech3=group).all()
        us4=Register_user.objects.filter(ntech4=group).all()
        context={
        'us1':us1,
        'us2':us2,
        'us3':us3,
        'us4':us4,
        'group':group,
        }
        return render(request,'nontech.html',context=context)
    else:
        return HttpResponseRedirect(reverse('login_user'))

def material(request):
    return render(request,'syllabus_page.html')


def contact(request):
    if request.method=='POST':
        print(request.POST['email'])
        a=request.POST['email']
        msg = EmailMessage('Message from ' + ' ' + a,
                       request.POST['msg'], to=['iamdeveloper3553@gmail.com'])
        msg.send()
        print("mail sent")
    return HttpResponseRedirect(reverse('user-dashboard',args=(request.session.get('name'),)))



def set_notice(request):
    if request.method=='POST':
        form =SetNoticeForm(request.POST)

        if form.is_valid():
            ls=Notice()
            ls.notice=form.cleaned_data['notice']
            ls.save()
            return HttpResponseRedirect(reverse('show_event'))

    else:
            form=SetNoticeForm()
    context={
    'form':form,
    }
    return render(request,'set_notice.html',context=context)


def set_event(request):
    if request.method=='POST':
        form =SetEventForm(request.POST)

        if form.is_valid():
            ls=Event()
            ls.event=form.cleaned_data['event']
            ls.date=form.cleaned_data['date']
            ls.time=form.cleaned_data['time']
            ls.venue=form.cleaned_data['venue']
            ls.save()
            return HttpResponseRedirect(reverse('show_event'))

    else:
            form=SetEventForm()
    context={
    'form':form,
    }
    return render(request,'set_event.html',context=context)


def show_event(request):
    ns=Event.objects.all()
    context={
    'ns':ns
    }
    return render(request,'show_event.html',context)



def delete_event(request,id):
    try:
        Notice.objects.filter(id=id).delete()
    except:
        pass
    return HttpResponseRedirect(reverse('show_event'))
