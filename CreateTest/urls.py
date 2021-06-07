from django.urls import path
from . import views
from Test import views as testViews
from CreateTest import views as createViews

app_name = 'create'
urlpatterns = [
    path('edit/question/<str:idquest>/delete',createViews.deleteQuestion,name='questionDelete'),
    path('edit/question/<str:idquest>/preview',createViews.PrevQuestion.as_view(),name='questionPrev'),
    path('edit/question/<str:idquest>/',createViews.EditQuestion.as_view(),name='questionID'),
    path('edit/question',createViews.QuestionList.as_view(),name='question'),
    path('edit/welcome/preview',createViews.welcomePrev,name='welcomeprev'),
    path('edit/welcome',createViews.EditWelcome.as_view(),name='welcome'),
    path('edit/info', createViews.UpdateInfo.as_view(),name='info'),
    path('edit', createViews.editTest,name='edit'),
    path('login',createViews.authorLogin,name='login'),
    path('info', createViews.info,name='signup'),
    path('', createViews.index,name='index')
]
