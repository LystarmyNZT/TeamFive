from django.urls import path, re_path

from . import views

urlpatterns=[
    path('createreq/',views.createreq,name='createreq'),
    path('reqprogress',views.reqprogress,name='reqprogress'),
    path('outputpdf/<int:id>/',views.outputpdf,name='outputpdf'),
    path('deletereq/<int:id>/',views.deletereq,name='deletereq'),

    path('askapproval/',views.askapproval,name='askapproval'),
    path('askapproval/<int:reqid>/<int:id>',views.askapproval,name='askapproval'),
    path('askedreq/',views.askedreq,name='askedreq'),
    path('askedreq/<int:reqid>/<int:id>',views.askedreq,name='askedreq'),
]