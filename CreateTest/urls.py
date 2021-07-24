from django.urls import path
from . import views
from Test import views as testViews
from CreateTest import views as createViews

app_name = 'create'
urlpatterns = [
    # path('edit/report',createViews.TestReport.as_view(),name='testReport'),
    # path('edit/question/<str:idquest>/delete',createViews.deleteQuestion,name='questionDelete'),
    # path('edit/question/<str:idquest>/preview',createViews.PrevQuestion.as_view(),name='questionPrev'),
    # path('edit/question/<str:idquest>/',createViews.EditQuestion.as_view(),name='questionID'),
    # path('edit/question',createViews.QuestionList.as_view(),name='question'),
    # path('edit/testtaker/<str:testTakerID>/delete',createViews.testTakerDelete,name='takerDelete'),
    # path('edit/testtaker/<str:testTakerID>/',createViews.TestTakerDetail.as_view(),name='takerDetail'),
    # path('edit/welcome/preview',createViews.welcomePrev,name='welcomeprev'),
    # path('edit/welcome',createViews.EditWelcome.as_view(),name='welcome'),
    # path('edit/info', createViews.UpdateInfo.as_view(),name='info'),
    # path('edit/testTaker', createViews.TestTakerList.as_view(),name='testTaker'),
    path('edit', createViews.editTest,name='edit'),
    path('login',createViews.authorLogin,name='login'),
    # path('new', createViews.newTest,name='newTest'),
    path('', createViews.index,name='firstPage')
]
