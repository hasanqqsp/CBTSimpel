from django.urls import path
from . import views
from Test import views as testViews
from CreateTest import views as createViews

app_name = 'test'
urlpatterns = [
#     path('viewscore/<str:session_key>/print',testViews.generate_pdf, name='viewscoreprint'),    
#     path('viewscore/<str:session_key>/',testViews.viewScore, name='viewscore'),
    path('sessioninfo/', testViews.sessionInfo, name = 'sessionInfo'),
    path('createsession/<str:testID>', testViews.createSession, name = 'createSession'),
    path('<str:testID>/q/welcome' ,testViews.welcomeTest, name='welcome'),
    path('<str:testID>/q/verify' ,testViews.verifyAnswer, name='verify' ),
    path('<str:testID>/q/<str:questID>' ,testViews.doTest, name='question'),
    path('<str:testID>/' ,testViews.detailTest, name='detail'),
#    path('', testViews.index ),
    path('cancel/r/<str:redirID>' ,testViews.cancelTest),
    path('test',testViews.showTest),
    path('resume',testViews.resumeTest, name = 'resume'),
    path('join',testViews.joinTest, name='join'),
]