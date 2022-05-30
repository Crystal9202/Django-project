from django.urls import path
from . import views

urlpatterns = [
    path('index' ,views.index , name = 'index') ,
    path('login' , views.login , name='login') ,
    path('create' , views.create , name= "create") ,
    path('revise' ,views.revise , name="revise") ,
    path('delete' ,views.delete , name="delete") ,
    path('finish' ,views.finish , name= "finish") ,
    path('schedule' , views.schedule , name="schedule") ,
    path('test' , views.test , name="test"),
    path('depsform' , views.depsform , name="depsform")
]