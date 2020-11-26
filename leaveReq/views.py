import hashlib

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from teamfive import settings
from users.models import stu,teacher
from leaveReq.models import reqforleave
# Create your views here.

def createreq(request):
    if request.session['is_teacher']==True:
        is_teacher=True
    else:
        is_teacher=False

    if request.method=="POST":
        reason1=request.POST.get('reason')
        destin1=request.POST.get('destin')
        timestart1 = request.POST.get('timestart')
        timefinish1 = request.POST.get('timefinish')
        try:
            stu1=stu.objects.get(sid=request.session.get('userid'))
            req1=reqforleave(stu=stu1,reason=reason1,destin=destin1,timestart=timestart1,timefinish=timefinish1)
            req1.save()
        except:
            message="请假条生成失败"
        return render(request, 'user/index.html',locals())
    return render(request,'leavereq/createreq.html',locals())

def reqprogress(request):
    if request.session['is_teacher']==True:
        is_teacher=True
    else:
        is_teacher=False

    stu1 = stu.objects.get(sid=request.session.get('userid'))
    reqs=reqforleave.objects.filter(stu=stu1,is_finished="False")
    for req in reqs:
        req.count=(req.process1+req.process2+req.process3)*100/3
    return render(request,'leavereq/reqprogress.html',locals())

def font_patch():
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics
    from xhtml2pdf.default import DEFAULT_FONT
    pdfmetrics.registerFont(TTFont('yh', '{}/font/msyh.ttf'.format(
        settings.STATICFILES_DIRS[0])))
    DEFAULT_FONT['helvetica'] = 'yh'

def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def outputpdf(request,id):

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename='请假条.pdf'"
    areq = reqforleave.objects.get(id=id)
    pri=str(areq.id)+str(areq.stu.sinstitute)+str(areq.stu.ssupervisor)+str(areq.timestart)+str(areq.timefinish)
    print(pri)
    areq.hash256=hash_code(pri)
    html = render_to_string("leavereq/pdf.html", locals())
    font_patch()
    status = pisa.CreatePDF(html,dest=response)

    if status.err:
        return HttpResponse("PDF文件生成失败")
    return response

def deletereq(request,id):
    print(id)
    deletereq=reqforleave.objects.get(id=id)
    deletereq.is_finished=True
    deletereq.save()
    return redirect('/leavereq/reqprogress')

def askapproval(request,reqid=None,id=None):
    ''''''
    if id==None:
        teacher1=teacher.objects.get(tid=request.session.get('userid'))
        ins_id=teacher1.tins.id
        if teacher1.trole=="辅导员":
            reqs=reqforleave.objects.filter(process1=0)
        elif teacher1.trole=="导师":
            sup_id=teacher1.id
            reqs=reqforleave.objects.filter(process2=0)

        elif teacher1.trole=="院长":
            reqs=reqforleave.objects.filter(process3=0)
        for req in reqs:
            req.count = (req.process1 + req.process2 + req.process3) * 100 / 3
        return render(request, 'leavereq/askapproval.html', locals())
    elif id==1:
        req = reqforleave.objects.get(id=reqid)
        req.process1=1
        req.save()
        return redirect('/leavereq/askapproval')
    elif id==2:
        req = reqforleave.objects.get(id=reqid)
        req.process2 = 1
        req.save()
        return redirect('/leavereq/askapproval')
    elif id==3:
        req = reqforleave.objects.get(id=reqid)
        req.process3 = 1
        req.save()
        return redirect('/leavereq/askapproval')

def askedreq(request,reqid=None,id=None):
    ''''''
    if id==None:
        teacher1=teacher.objects.get(tid=request.session.get('userid'))
        ins_id=teacher1.tins.id
        if teacher1.trole=="辅导员":
            reqs=reqforleave.objects.filter(process1=1)
        elif teacher1.trole=="导师":
            sup_id=teacher1.id
            reqs=reqforleave.objects.filter(process2=1)
        elif teacher1.trole=="院长":
            reqs=reqforleave.objects.filter(process3=1)
        for req in reqs:
            req.count = (req.process1 + req.process2 + req.process3) * 100 / 3
        return render(request, 'leavereq/askapproval.html', locals())
    elif id==1:
        req = reqforleave.objects.get(id=reqid)
        req.process1=0
        req.save()
        return redirect('/leavereq/askapproval')
    elif id==2:
        req = reqforleave.objects.get(id=reqid)
        req.process2 = 0
        req.save()
        return redirect('/leavereq/askapproval')
    elif id==3:
        req = reqforleave.objects.get(id=reqid)
        req.process3 = 0
        req.save()
        return redirect('/leavereq/askapproval')