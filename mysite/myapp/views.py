from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Student, Conversation, Message, Profile
from .forms import StudentForm
import random
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db.models import Count
# Create your views here.
#def home(request):
    #return HttpResponse("my first try go")

def home(request):
    context = {
        'name' : 'Seun',
        'message' : 'we are always happy to see you always.'
    }
    return render(request,"myapp/home.html",context)
def about(request):
    context = {
        'title' : 'About us',
        'content' : 'we are the latest developer in town.'
    }
    return render(request,"myapp/about.html",context)

def students(request):
    data = Student.objects.all()
    return render(request, 'myapp/students.html', {'students':data})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('students')
    else:
        form = StudentForm()

    return render(request, 'myapp/add-student.html', {'form': form})

def edits(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.department = request.POST.get('department')
        student.level = request.POST.get('level')
        student.save()
        return redirect('students')

    return render(request, 'myapp/edit.html', {'student': student})

def dels(request,  id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        student.delete()
        return redirect('students')
    return render(request, 'myapp/del.html', {'student': student})

def add(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        department=request.POST.get('department')
        level=request.POST.get('level')
        email=request.POST.get('email')
        otp=str(random.randint(100000,999999))
        send_mail(
            subject = 'App verification',
            message = f'your otp is: {otp}',
            from_email = None,
            recipient_list = [email],
            fail_silently = False, 
        )
        request.session['name'] = name
        request.session['department'] = department
        request.session['level'] = level
        request.session['email'] = email
        request.session['otp'] = otp

        
        return redirect('otp')
    return render(request, 'myapp/add.html')

def otp_v(request):
    name = request.session.get('name')
    department = request.session.get('department')
    level = request.session.get('level')
    email = request.session.get('email')
    otp = request.session.get('otp')

    if not otp:
        return redirect('add')
    
    if request.method == 'POST':
        otp2 = request.POST.get('otp')
        if otp2 == otp:
            Student.objects.create(
                name=name,
                department=department,
                level=level,
                email=email
            )
            request.session.flush()
            return redirect('students')
        else:
            error ='incorrect otp'
            return render(request, 'myapp/otp.html', {'error':error})
    return render(request, 'myapp/otp.html')



def log_in(request):
    return redirect('login')

def login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        level = request.POST.get('level')

        try:
            student = Student.objects.get(name=name, level=level)
            request.session['student_id']=student.id
            return redirect('dash')
        except Student.DoesNotExist:
            error='incorrect name or level'
            return render(request, 'myapp/login.html', {'error':error})
    return render(request, 'myapp/login.html')

def logout(request):
    request.session.flush()
    return redirect('login')

def dash(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')

    student = Student.objects.get(id=student_id)
    email = student.email
    request.session['myemail'] = email
    if User.objects.filter(username=email).exists():
        user = User.objects.get(username=email)
    else:
        user = User.objects.create_user(username=email, password='user123')

    if Profile.objects.filter(user = user).exists():
        myself = Profile.objects.get(user = user)
    else:
        myself = Profile.objects.create(user = user)
    if request.method == 'POST':
        friend_e=request.POST.get('email')
        if friend_e == email:
            return HttpResponse(status=204)
        try:
            student = Student.objects.get(email=friend_e)
            if User.objects.filter(username=friend_e).exists():
                user_f = User.objects.get(username=friend_e)
            else:
                user_f = User.objects.create_user(username=friend_e, password='user123')
            if Profile.objects.filter(user = user_f).exists():
                myfriend = Profile.objects.get(user = user_f)
            else:
                myfriend = Profile.objects.create(user = user_f)
            myself.friends.add(myfriend)
            return HttpResponse(status=204)
        except Student.DoesNotExist:
            return HttpResponse(status=204)
    added_f=myself.friends.all()
    return render(request, 'myapp/dash.html', {'student':student, 'friends':added_f})

def chat(request):
    if request.method == 'POST':
        friend_email = request.POST.get('email')
        request.session['friend_email']=friend_email
    return redirect('send_message')

def send_message(request):
    my_email = request.session.get('myemail')
    friend_email = request.session.get('friend_email')
    user = User.objects.get(username=my_email)
    friend = User.objects.get(username=friend_email)
    myself = Profile.objects.get(user = user)
    myfriend = Profile.objects.get(user = friend)
    existing = Conversation.objects.filter(participants=user).filter(participants=friend).first()
    
    if existing:
        conversation = existing
    else:
        conversation = Conversation.objects.create()
        conversation.participants.add(user, friend)
    messages = conversation.messages.all()
    if request.method == 'POST':
        message = request.POST.get('msg')
        file = request.FILES.get('file')
        myfriend.friends.add(myself)
        Message.objects.create(conversation = conversation, sender = user, content = message, file = file)
        return HttpResponse(status=204)
    return render(request, 'myapp/send.html',{'friend':friend_email, 'messages': messages, 'user': user})

def clear(request):
    if request.method == "POST":
        my_email = request.session.get("myemail")
        friend_email = request.POST.get("friend_email")

        user = User.objects.get(username=my_email)
        friend = User.objects.get(username=friend_email)

        # Get the conversation
        conversation = Conversation.objects.filter(participants=user).filter(participants=friend).first()
        if conversation:
            Message.objects.filter(conversation=conversation).delete()
        return HttpResponse(status=204)
    return redirect('send_message')

def delete_friend(request):
    if request.method == "POST":
        my_email = request.session.get("myemail")
        friend_email = request.POST.get("email")

        user = User.objects.get(username=my_email)
        friend = User.objects.get(username=friend_email)

        my_profile = Profile.objects.get(user=user)
        friend_profile = Profile.objects.get(user=friend)

        my_profile.friends.remove(friend_profile)
        
        return HttpResponse(status=204)
    return redirect('dash')