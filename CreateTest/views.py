from django.shortcuts import render,get_object_or_404
from django import forms

# from CreateTest import forms as createTestForms
from Test.forms import LoginForm 
# from django.views.generic.edit import UpdateView 
from Test.models import (Question , TestPackage, Answer, TestTaker)
from django.urls import reverse, reverse_lazy
from django.http import (HttpResponseRedirect ,HttpResponse)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
# from django.core import serializers
# from django.core.exceptions import ValidationError, PermissionDenied
# from django.utils.translation import gettext as _
from django.contrib.auth.views import LoginView , LogoutView
# from django_quill.forms import QuillFormField
import random ,string, sys , datetime
from django.views.generic import ListView, UpdateView, DetailView, FormView, CreateView,TemplateView
from django.views.generic.edit import FormMixin

# Create your views here.
adminLoginURL = reverse_lazy('create:login')

# class GroupRequiredMixin(object):
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user:
#             return HttpResponseRedirect(adminLoginURL)
#         else:
#             if not request.user.groups.filter(name='author').exists():
#                 return HttpResponseRedirect(adminLoginURL)
#         return super(GroupRequiredMixin, self).dispatch(request, *args, **kwargs)

def isAdmin(request):
    if not request.user.groups.filter(name='creator').exists():
        return HttpResponseRedirect(adminLoginURL)

# def viewScoreQuery(session_key):
#     findTestTaker = get_object_or_404(TestTaker, session_key = session_key)
#     answerQuery = Answer.objects.filter(session_key=session_key)
#     packQuery = TestPackage.objects.get(testID=findTestTaker.testID)
#     questQuery = Question.objects.filter(testID=findTestTaker.testID).order_by('questionNum')
#     query = []
#     score_obtained = 0
#     for i in answerQuery:
#         score_obtained += i.scoreObtain
#     findTestTaker.scoreObtained = score_obtained
#     findTestTaker.save()
#     for i in range(len(questQuery)):
#         try:
#             nth_answer = Answer.objects.get(testID=findTestTaker.testID,session_key=session_key,num_ofAnswer__exact=i+1)
#             scoreObtain = nth_answer.scoreObtain
#             i_answer = nth_answer.answer
#         except: 
#             scoreObtain = 0
#             i_answer = ""
        
#         if i_answer == 'A':
#                 answer = '{}'.format(questQuery[i].choiceFirst)
#         elif i_answer == 'B':
#             answer = '{}'.format(questQuery[i].choiceSecond)
#         elif i_answer == 'C':
#             answer = '{}'.format(questQuery[i].choiceThird)
#         elif i_answer == 'D':
#             answer = '{}'.format(questQuery[i].choiceFourth)
#         elif i_answer == 'E':
#             answer = '{}'.format(questQuery[i].choiceFifth)
#         elif i_answer == 'F':
#             answer = '{}'.format(questQuery[i].choiceSixth)
#         else:
#             answer = 'Error'
            
#         query.append({
#             'num':'{}'.format(questQuery[i].questionNum),
#             'question':questQuery[i].question,
#             'answer':"{}".format(answer),
#             'questID':'{}'.format(questQuery[i].questID),
#             'score':"{}".format(scoreObtain)})
#     return query

def index(request):
    return render(request,'CreateTest/index.html')

# def generate_testCode():
#     '''Generate an 6-character Integer'''
#     rand = ''.join([random.choice(string.digits) for n in range(6)])
#     if len(TestPackage.objects.filter(testCode=rand)) > 0 :
#         return self.generate_testcode()
#     else:
#         return rand

# def info(request):
#     if request.method == 'POST':
#         createTestForm = createTestForms.CreateTestPackage(request.POST or None)
#         if createTestForm.is_valid():
#             createTestForm = createTestForm
#             if request.POST.get('testCode'):
#                 createTestForm = createTestForm
#                 try:
#                     TestPackage.objects.get(testCode=request.POST.get('testCode'))
#                     createTestForm.add_error(error=ValidationError('Kode tidak dapat digunakan'),field='testCode')
#                     return render(request,'CreateTest/info.html',{'form':createTestForm})
#                 except:
#                     testCode = request.POST.get('testCode')
#             else:
#                 testCode = generate_testCode()
#             testCode = request.POST.get('testCode')
#             TestPackage.objects.create(
#                 testCode = testCode,
#                 testTitle = request.POST.get('testTitle'),
#                 testAuthor = request.POST.get('testAuthor'),
#                 testSchedule = request.POST.get('testSchedule'),
#                 timeLimit =  request.POST.get('timeLimit'),
#                 passwordAdminTest = request.POST.get('passwordAdminTest'),
#                 passwordTest = request.POST.get('passwordTest'),
#             )
            
#             credential = authenticate(request, username=testCode, password=request.POST.get('passwordAdminTest'))
#             return HttpResponseRedirect('/createtest/edit')
#     else :
#         createTestForm = createTestForms.CreateTestPackage
#     context = {
#         'form' : createTestForm
#     }
    
#     return render(request,'CreateTest/info.html',context)

def authorLogin(request):
    isAdmin(request)
    if request.method == 'POST':
        loginForm = LoginForm(request.POST or None)
        if loginForm.is_valid():
            loginForm = LoginForm(request.POST)
            credential = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'),)
            try:
                TestPackage.objects.get(testCode = request.POST.get('username'))
                if credential == None:
                    loginForm.add_error(error=ValidationError(''),field='password')
                else:
                    login(request,credential)
                    return HttpResponseRedirect('/createtest/edit')
            except:
                loginForm.add_error(error=ValidationError(''),field='username')
                    
    else :
        loginForm = LoginForm
    context = {
        'form' : loginForm
    }
    return render(request,'CreateTest/adminLogin.html',context)

# def editTest(request):
#     isAdmin(request)
#     query = TestPackage.objects.get(testCode=request.user) 
#     context = {
#         'testInfo': query,
#     }
#     return render(request,'CreateTest/dashboard.html', context)

# class EditQuestion(GroupRequiredMixin,UpdateView):
#     model = Question
#     form_class = createTestForms.QuestionForm
#     template_name = 'CreateTest/editQuestion.html'
#     success_url = '/createtest/edit/question'
    
#     def get_object(self):
#         testID = TestPackage.objects.get(testCode= self.request.user)
#         idQuest = self.kwargs.get('idquest')
#         obj = self.model.objects.get(questID=idQuest)
#         return obj
#     def get(self, request, *args, **kwargs):
#         testPackage = TestPackage.objects.get(testCode= self.request.user)
#         questQuery = Question.objects.filter(testID=testPackage.testID).order_by('-questionNum')
#         if self.kwargs.get('idquest') == 'new':
#             if len(Question.objects.filter(testID=testPackage.testID)) < 1:
#                 a = Question.objects.create(question="",testID=testPackage.testID,questionNum=1)
#             else:
#                 a = Question.objects.create(question="",testID=testPackage.testID,questionNum=questQuery[0].questionNum+1,testPackage=testPackage)
#             return HttpResponseRedirect("{}/{}".format(self.success_url, a.questID))
#         else:
#             self.object = self.get_object()
#             return self.render_to_response(self.get_context_data())

#     def get_context_data(self, **kwargs):
#         idQuest = self.kwargs.get('idquest')
#         testID = TestPackage.objects.get(testCode= self.request.user).testID
#         context = super(EditQuestion, self).get_context_data(**kwargs)
#         questQuery = self.model.objects.get(questID=idQuest)
#         queryset = self.model.objects.get(questID=idQuest)
#         questionList = self.model.objects.filter(testID=testID).order_by('questionNum')
#         CHOICES = [
#             ("A",queryset.choiceFirst),
#             ("B" ,queryset.choiceSecond),
#             ("C",queryset.choiceThird),
#             ("D",queryset.choiceFourth),
#             ("E",queryset.choiceFifth),
#             ("F",queryset.choiceSixth),
#         ]
#         context['choice'] = [
#             {'choice': questQuery.choiceFirst},
#             {'choice': questQuery.choiceSecond},
#             {'choice': questQuery.choiceThird},
#             {'choice': questQuery.choiceFourth},
#             {'choice': questQuery.choiceFifth},
#             {'choice': questQuery.choiceSixth},
#         ]
#         context['form'].initial = {
#             'question' : queryset.question,
#             'choice1' : queryset.choiceFirst, 
#             'choice2' : queryset.choiceSecond, 
#             'choice3' : queryset.choiceThird, 
#             'choice4' : queryset.choiceFourth, 
#             'choice5' : queryset.choiceFifth, 
#             'choice6' : queryset.choiceSixth, 
#             'answerKey' : queryset.answerKey,
#             'trueScore' : queryset.trueScore,
#             'falseScore' : queryset.falseScore
#         }
#         answerKey = queryset.answerKey
#         if queryset.answerKey == "A":
#             answerKey = queryset.choiceFirst
#         elif queryset.answerKey == "B":
#             answerKey = queryset.choiceSecond
#         elif queryset.answerKey == "C":
#             answerKey = queryset.choiceThird
#         elif queryset.answerKey == "D":
#             answerKey = queryset.choiceFourth
#         elif queryset.answerKey == "E":
#             answerKey = queryset.choiceFifth
#         elif queryset.answerKey == "F":
#             answerKey = queryset.choiceSixth
#         else:
#             answerKey = ""

#         context['answerKey'] = answerKey
#         context['question_list'] = questionList
#         context['form'].base_fields['answerKey'].choices = CHOICES
#         print(context['form'].base_fields['answerKey'].choices)
#         return context
#     def get_success_url(self):
#         if not self.success_url:
#             raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
#         self.success_url = "{}/{}".format(self.success_url,self.get_object().questID)
#         return str(self.success_url)  # success_url may be lazy

        
#     def form_valid(self, form,request):
#         self.object = self.get_object()
#         object = self.get_object()
        
#         if request.POST.get('question'):
#             object.question = eval(request.POST.get('question'))['html']
#         if request.POST.get('choice1'):
#             object.choiceFirst = eval(request.POST.get('choice1'))['html']
#             object.save()
#         if request.POST.get('choice2'):
#             object.choiceSecond = eval(request.POST.get('choice2'))['html']
#             object.save()
#         if request.POST.get('choice3'):
#             object.choiceThird = eval(request.POST.get('choice3'))['html']
#             object.save()
#         if request.POST.get('choice4'):
#             object.choiceFourth = eval(request.POST.get('choice4'))['html']
#             object.save()
#         if request.POST.get('choice5'):
#             object.choiceFifth = eval(request.POST.get('choice5'))['html']
#             object.save()
#         if request.POST.get('choice6'):
#             object.choiceSixth = eval(request.POST.get('choice6'))['html']
#             object.save()
#         if request.POST.get('answerKey'):
#             object.answerKey = request.POST.get('answerKey')
#             object.save()
#         if request.POST.get('trueScore'):
#             print(request.POST.get('trueScore'))
#             object.trueScore = request.POST.get('trueScore')
#             object.save()
#         if request.POST.get('falseScore'):
#             object.falseScore = request.POST.get('falseScore')
#             object.save()
#         # object.question = request.POST.get('question')
#         # object.choiceFirst = request.POST.get('choice1')
#         # object.choiceSecond = request.POST.get('choice2')
#         # object.choiceThird = request.POST.get('choice3')
#         # object.choiceFourth = request.POST.get('choice4')
#         # object.choiceFifth = request.POST.get('choice5')
#         # object.choiceSixth = request.POST.get('choice6')
#         # object.answerKey = request.POST.get('answerKey')
#         # object.save()

#         object.save()
#         return HttpResponseRedirect(self.get_success_url())

#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         return self.form_valid(form,request)
             
# class PrevQuestion(GroupRequiredMixin,TemplateView):
#     template_name = "Test/doTest.html"
#     querytest = ""
#     json_serializer  = ""
#     querysets = ""
#     json_question = ""
#     questionList = ""
#     def queryset(self, **kwargs):
#         self.querytest = TestPackage.objects.get(testCode=self.request.user)
#         self.json_serializer = serializers.get_serializer("json")()
#         self.questionList = Question.objects.filter(testID=self.querytest.testID)
#         self.querysets = Question.objects.get(questID=self.kwargs.get('idquest'), testID=self.querytest.testID)
#         self.json_question = self.json_serializer.serialize(self.questionList, ensure_ascii=False)

#     def get_context_data(self, **kwargs):
#         self.queryset()
#         kwargs.setdefault('view', self)
#         CHOICES = [self.querysets.choiceFirst,self.querysets.choiceSecond,
#         self.querysets.choiceThird,self.querysets.choiceFourth,self.querysets.choiceFifth,
#         self.querysets.choiceSixth,
#         ]
#         kwargs.update({
#                 'is_preview' : True,
#                 'question' : self.querysets,
#                 'json_q': self.json_question,
#                 'testInfo': self.querytest,
#                 'question_list' : self.questionList,
#                 'choices': CHOICES
#         })

#         return kwargs

# def deleteQuestion(request,idquest):
#     isAdmin(request)
#     success_url = '/createtest/edit/question'
#     get_object = Question.objects.get(questID=idquest)
#     get_object.delete()
#     return HttpResponseRedirect(success_url)

# def welcomePrev(request):
#     isAdmin(request)
#     packQuery = TestPackage.objects.get(testCode=request.user)
#     welcomeQuery = TestWelcome.objects.get(testID=packQuery.testID)
#     context={
#         'welcome' : welcomeQuery
#     }
#     return render(request,'CreateTest/welcomePagePrev.html', context)

#     welcomeMessage = QuillFormField()

# class EditWelcome(GroupRequiredMixin,UpdateView):
#     model = TestWelcome
#     form_class = createTestForms.WelcomeMessage
#     template_name = 'CreateTest/welcomePage.html'
#     success_url = '/createtest/edit/welcome'
#     def get_object(self ,queryset=None):
#         testQuery = TestPackage.objects.get(testCode = self.request.user)
#         obj,create = self.model.objects.get_or_create(testID = testQuery.testID)
#         return obj

#     def post(self, request, *args, **kwargs):    
#         form = self.get_form()
#         self.object = self.get_object()
#         if request.POST.get('welcomeMessage'):
#             return self.form_valid(request)
#         else:
#             return self.form_invalid(form)

#     def get_context_data(self, **kwargs):
#         context = super(EditWelcome, self).get_context_data(**kwargs)
#         obj = self.get_object(self)
#         context['form'].initial = {
#             'welcomeMessage' : obj.welcomeMessage
#         }
#         return context
#     def form_valid(self, request, *args, **kwargs):
#         obj = self.get_object()
#         obj.welcomeMessage = eval(request.POST.get('welcomeMessage'))['html']
#         obj.save()
#         return HttpResponseRedirect(self.get_success_url())
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return self.render_to_response(self.get_context_data())

# class UpdateInfo(GroupRequiredMixin,UpdateView):
#     model = TestPackage
#     def get_object(self ,queryset=None):
#         obj = self.model.objects.get(testCode=self.request.user)
#         return obj
#     def post(self, request, *args, **kwargs):    
#         form = self.get_form()
#         self.object = self.get_object()
#         if request.POST.get('csrfmiddlewaretoken'):
#             return self.form_valid(request)
#         else:
#             return self.form_invalid(form)
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
    
#     def form_valid(self, request, *args, **kwargs):
#         obj = self.get_object()
#         obj.testTitle = request.POST.get('testTitle')
#         obj.testAuthor = request.POST.get('testAuthor')
#         obj.testSchedule = request.POST.get('testSchedule')
#         obj.timeLimit = request.POST.get('timeLimit')
#         obj.passwordTest = request.POST.get('passwordTest')
#         obj.passwordAdminTest = request.POST.get('passwordAdminTest')
#         obj.save()
#         return HttpResponseRedirect(self.get_success_url())

#     template_name = 'CreateTest/updateInfo.html'
#     form_class = createTestForms.UpdateTestInfo
#     success_url = '/createtest/edit'
    
# class QuestionList(GroupRequiredMixin,ListView):
#     template_name = 'CreateTest/question.html'
#     def get_queryset(self):
#         testID = TestPackage.objects.get(testCode= self.request.user).testID
#         queryset = Question.objects.filter(testID=testID).order_by('questionNum')
#         return queryset

# class TestTakerList(GroupRequiredMixin,FormMixin,ListView):
#     template_name = 'CreateTest/testTakerList.html'
#     form_class = createTestForms.AddTestTakerForm
#     def get_queryset(self):
#         testID = TestPackage.objects.get(testCode= self.request.user).testID
#         queryset = TestTaker.objects.filter(testID=testID)
#         return queryset
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["timeLimit"] = TestPackage.objects.get(testCode =  self.request.user).timeLimit
#         return context
#     def form_valid(self, form):
#         obj = form.save(commit=False)
#         obj.testID = TestPackage.objects.get(testCode= self.request.user).testID
#         obj.save()
#         return HttpResponseRedirect('/createtest/edit/testTaker')
#     def form_invalid(self, form):
#         return self.render_to_response(self.get_context_data(form=form))
#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         if form.is_valid():
#             print(form.data)
#             form.save()
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

# def testTakerDelete(request,testTakerID):
#     isAdmin(request)
#     success_url = '/createtest/edit/testTaker'
#     get_object = TestTaker.objects.get(testTakerID=testTakerID)
#     get_object.delete()
#     return HttpResponseRedirect(success_url)

# class TestTakerDetail(GroupRequiredMixin,DetailView):
#     model = TestTaker
#     template_name = 'CreateTest/testTakerDetail.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["timeLimit"] = TestPackage.objects.get(testCode =  self.request.user).timeLimit
#         session_key = context["object"].session_key
#         context["query"] = viewScoreQuery(session_key)
#         return context
#     def get_object(self):
#         obj = self.model.objects.get(testTakerID=self.kwargs.get('testTakerID'))
#         return obj

# class TestReport(GroupRequiredMixin,TemplateView):
#     modelTestPackage = TestPackage
#     modelTestReport = TestReport
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["testQuery"] = self.modelTestPackage.objects.get(testCode=self.request.user)
#         context["reportQuery"] = self.modelTestReport.objects.get()
#         return context
    
#     template_name = 'CreateTest/report.html'