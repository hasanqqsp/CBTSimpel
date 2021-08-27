from django.urls import path
from . import views
from Test import views as testViews
from CreateTest import views as createViews
from django.views.generic import ListView, FormView
from CreateTest.forms import QuestionForm
from Test.models import Question
app_name = 'create'
urlpatterns = [
    # path('edit/report',createViews.TestReport.as_view(),name='testReport'),
    path('question/<str:questID>/delete',createViews.QuestionDelete.as_view(),name='questionDelete'),
    # path('edit/question/<str:idquest>/preview',createViews.PrevQuestion.as_view(),name='questionPrev'),
    path('question/<str:questID>/',createViews.QuestionEdit.as_view(),name='questionEdit'),
    path('questions/new',createViews.QuestionCreate.as_view(),name='newQuestion'),
    path('questions',createViews.QuestionsList.as_view(),name='questions'),
    path('edit/testTaker/<str:testTakerID>/delete',createViews.TestTakerDelete.as_view(),name='testTakerDelete'),
    # path('edit/testtaker/<str:testTakerID>/',createViews.TestTakerDetail.as_view(),name='takerDetail'),
    # path('edit/welcome/preview',createViews.welcomePrev,name='welcomeprev'),
    path('welcomePage/edit',createViews.WelcomePageEdit.as_view(),name='welcomePageEdit'),
    # path('edit/info', createViews.UpdateInfo.as_view(),name='info'),
    path('export/testTaker/xls',createViews.exportTestTakerXls,name='exportTestTakerXls'),
    path('exportimport',createViews.ExportImport.as_view(),name="exportImport"),
    path('testTaker', createViews.TestTakerList.as_view(),name='testTakerList'),
    path('config/advance',createViews.AdvanceConfigView.as_view(),name='advanceConfig'),
    path('config/basic',createViews.BasicConfigView.as_view(),name='basicConfig'),
    path('dashboard', createViews.dashboard,name='dashboard'),
    path('login',createViews.authorLogin,name='login'),
    path('logout',createViews.AuthorLogout.as_view(),name='logout'),
    path('new', createViews.NewTest.as_view(),name='newTest'),
    path('', createViews.index,name='firstPage')
]
