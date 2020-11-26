from django.shortcuts import render,redirect
import hashlib
from users.models import stu,teacher,institute


def login(request):

    if request.session.get("is_login"):
        return redirect('/index')
    if request.method=="POST":
        userid=request.POST.get('userid')
        password=request.POST.get('password')
        try:
            print("hello")
            if stu.objects.filter(sid=userid).exists():
                stu1 = stu.objects.get(sid=userid)
                if stu1.spassword==hash_code(password) or (stu1.spassword=="123456" and password=="123456"):
                    request.session['is_teacher']=False
                    request.session['is_login']=True
                    request.session['userid']=stu1.sid
                    request.session['username']=stu1.sname
                    is_teacher=False
                    return redirect('/index/')
                else:
                    message="密码不正确！"
            elif teacher.objects.filter(tid=userid).exists():
                teacher1 = teacher.objects.get(tid=userid)
                if teacher1.tpassword == hash_code(password) or (teacher1.tpassword == "123456" and password == "123456"):
                    request.session['is_teacher'] = True
                    request.session['is_login'] = True
                    request.session['userid'] = teacher1.tid
                    request.session['username'] = teacher1.tname
                    is_teacher=True
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
        except:
            message="用户名不存在！"
        return render(request, 'user/login.html',locals())
    return render(request,'user/login.html')

def index(request):
    if request.session['is_teacher']==True:
        is_teacher=True
    else:
        is_teacher=False

    return render(request,'user/index.html',locals())

def logout(request):
    if not request.session.get('is_login'):
        return redirect("/login/")
    request.session.flush()
    return redirect("/login/")

def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def changepwd(request):
    if request.session['is_teacher']==True:
        is_teacher=True
    else:
        is_teacher=False

    if request.method=="POST":
        currpwd=request.POST.get('currpwd')
        newpwd=request.POST.get('newpwd')
        try:
            if stu.objects.filter(sid=request.session.get('userid')).exists():
                stu1=stu.objects.get(sid=request.session.get('userid'))
                if stu1.spassword==hash_code(currpwd) or stu1.spassword=="123456" :
                    stu1.spassword=hash_code(newpwd)
                    stu1.save()
                    return redirect('/index/',locals())
                else:
                    message="当前密码不正确！"
            elif teacher.objects.filter(tid=request.session.get('userid')).exists():
                teacher1=teacher.objects.get(tid=request.session.get('userid'))
                if teacher1.tpassword==hash_code(currpwd) or teacher1.tpassword=="123456" :
                    teacher1.tpassword=hash_code(newpwd)
                    teacher1.save()
                    return redirect('/index/',locals())
                else:
                    message="当前密码不正确！"
        except:
            message="用户不存在！"
        return render(request, 'user/login.html',locals())
    return render(request,'user/changepwd.html',locals())

def detail(request):
    if request.session['is_teacher']==True:
        is_teacher=True
    else:
        is_teacher=False

    if stu.objects.filter(sid=request.session.get('userid')).exists():
        this=stu.objects.get(sid=request.session.get('userid'))
        this.name=this.sname
        this.id=this.sid
        this.supervisor=this.ssupervisor
        this.institute=this.sinstitute
        this.phone=this.sphone
    elif teacher.objects.filter(tid=request.session.get('userid')).exists():
        this = teacher.objects.get(tid=request.session.get('userid'))
        this.name=this.tname
        this.id=this.tid
        this.role=this.trole
        this.institute=this.tins
        this.phone=this.tphone
    return render(request, 'user/detail.html', locals())
