from django.urls import path
from . import views
from Test import views as testViews
from CreateTest import views as createViews

app_name = 'test'
urlpatterns = [
    path('viewscore/<str:session_code>/pdf',testViews.generate_pdf, name='viewscoreprint'),    
    path('viewscore/<str:session_code>/',testViews.viewScore, name='viewscore'),
    path('viewscore/',testViews.findScore, name='findScore'),
    path('session/info', testViews.sessionInfo, name = 'sessionInfo'),
    path('session/edit', testViews.sessionEdit, name = 'sessionEdit'),
    path('createsession/<str:testID>', testViews.createSession, name = 'createSession'),
    path('<str:testID>/q/welcome' ,testViews.welcomeTest, name='welcome'),
    path('<str:testID>/q/verify' ,testViews.verifyAnswer, name='verify' ),
    path('<str:testID>/q/<str:questID>' ,testViews.doTest, name='question'),
    path('<str:testID>/' ,testViews.detailTest, name='detail'),
    path('cancel/r/<str:redirID>' ,testViews.cancelTest),
    path('test',testViews.showTest),
    path('resume',testViews.resumeTest, name = 'resume'),
    path('join',testViews.joinTest, name='join'),
]