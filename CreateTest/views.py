# from django.shortcuts import render
# from django import forms

# from CreateTest import forms as createTestForms
# from Test.forms import ResumeTestForm 
# from django.views.generic.edit import UpdateView 
# from Test.models import (Question , TestPackage, Answer, TestTaker,TestWelcome)
# from django.http import (HttpResponseRedirect ,HttpResponse)
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login,logout
# from django.core import serializers
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext as _
# from django.contrib.auth.views import LoginView,LogoutView
# from django_quill.forms import QuillFormField
# import random ,string, sys 
# from django.views.generic import ListView, UpdateView, DetailView, FormView, CreateView,TemplateView
# from utils.generate_id import generate_id

# # Create your views here.
# def index(request):
#     return render(request,'CreateTest/index.html')

# def info(request):
#     def generate_testCode():
#         '''Generate an 6-character Integer'''
#         rand = ''.join([random.choice(string.digits) for n in range(6)])
#         try:
#             # if this possible ID exists, run again:
#             TestPackage.objects.get(testCode=rand)
#             return self.generate_testcode()
#         except:
#             return rand
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
#                 testID= generate_id(TestPackage,'testID',16),
#                 testCode = testCode,
#                 testTitle = request.POST.get('testTitle'),
#                 testAuthor = request.POST.get('testAuthor'),
#                 testSchedule = request.POST.get('testSchedule'),
#                 timeLimit =  request.POST.get('timeLimit'),
#                 passwordAdminTest = request.POST.get('passwordAdminTest'),
#                 passwordTest = request.POST.get('passwordTest'),
#             )
            
#             credential = authenticate(request, username=testCode, password=request.POST.get('passwordAdminTest'))
#             print(credential)
#             login(request,credential)
#             return HttpResponseRedirect('/createtest/edit')
#     else :
#         createTestForm = createTestForms.CreateTestPackage
#     context = {
#         'form' : createTestForm
#     }
    
#     return render(request,'CreateTest/info.html',context)

# def authorLogin(request):
#     try : 
#         getTestPackage = TestPackage.objects.get(testCode=request.user)
#     except:
#         session = None

#     if request.user.is_authenticated :
#         return HttpResponseRedirect('/createtest/edit')
#     else :
#         if request.method == 'POST':
#             loginForm = ResumeTestForm(request.POST or None)
#             if loginForm.is_valid():
#                 loginForm = ResumeTestForm(request.POST)
#                 try:
#                     query = TestPackage.objects.get(testCode=request.POST.get('username'))
#                     credential = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'),)
#                     login(request,credential)
#                     return HttpResponseRedirect('/createtest/edit')
#                 except :
#                     loginForm.add_error(error=ValidationError('Tes dengan kode tersebut tidak ditemukan'),field='username')
#         else :
#             loginForm = ResumeTestForm
#     context = {
#         'form' : loginForm
#     }
#     return render(request,'Test/resume.html',context)

# def authorLogout(request):
#     logout(request)
#     return HttpResponseRedirect('/createtest/login')

# def questionList(request):
#     pass

# def editTest(request):
#     try:
#         query = TestPackage.objects.get(testCode=request.user) 
#     except :
#         return HttpResponseRedirect('/test/createsession/{}'.format(idtest))
#     context = {
#         'testInfo': query,
#     }
#     return render(request, 'CreateTest/dashboard.html', context)

# class EditQuestion(UpdateView):
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
#         testID = TestPackage.objects.get(testCode= self.request.user)
#         lastNum = Question.objects.filter(testID=testID.testID).order_by('-questionNum')
#         questID = generate_id(Question,'questID',16)
#         print(questID)
#         if lastNum.exists():
#             lastNum = lastNum[0].questionNum + 1
#         else :
#             lastNum = 1
#         if self.kwargs.get('idquest') == 'new':
#             a = Question.objects.create(question="",testID=testID.testID,questionNum=lastNum,questID=questID)
#             return HttpResponseRedirect("{}/{}".format(self.success_url, a.questID))
#         else:
#             self.object = self.get_object()
#             return self.render_to_response(self.get_context_data())

#     def get_context_data(self, **kwargs):
#         idQuest = self.kwargs.get('idquest')
    
#         context = super(EditQuestion, self).get_context_data(**kwargs)
#         questQuery = self.model.objects.get(questID=idQuest)
#         queryset = self.model.objects.get(questID=idQuest)
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
#             'answerKey' : queryset.answerKey

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
#         context['form'].base_fields['answerKey'].widget.choices = CHOICES
#         print(context['form'].base_fields['answerKey'].widget.choices)
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
            
#             object.save()
#         if request.POST.get('choice1'):
#             object.choiceFirst = eval(request.POST.get('choice1'))['html']
#             print(object.choiceFirst)
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

#         return HttpResponseRedirect(self.get_success_url())

#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         return self.form_valid(form,request)
             
# class PrevQuestion(TemplateView):
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

#         print(kwargs)
#         return kwargs

# def deleteQuestion(request,idquest):
#     success_url = '/createtest/edit/question'
#     get_object = Question.objects.get(questID=idquest)
#     get_object.delete()
#     return HttpResponseRedirect(success_url)

# def welcomePrev(request):
  
#     packQuery = TestPackage.objects.get(testCode=request.user)
#     welcomeQuery = TestWelcome.objects.get(testID=packQuery.testID)
#     context={
#         'welcome' : welcomeQuery
#     }
#     return render(request,'CreateTest/welcomePagePrev.html', context)

#     welcomeMessage = QuillFormField()

# class EditWelcome(UpdateView):
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
#         print(eval(request.POST.get('welcomeMessage'))['html'])
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

# class UpdateInfo(UpdateView):
#     model = TestPackage
#     def get_object(self ,queryset=None):
#         obj = self.model.objects.get(testCode=self.request.user)
#         return obj
#     template_name = 'CreateTest/updateInfo.html'
#     form_class = createTestForms.UpdateTestInfo
#     success_url = '/createtest/edit'
    
# class QuestionList(ListView):
#     template_name = 'CreateTest/question.html'
#     def get_queryset(self):
#         testID = TestPackage.objects.get(testCode= self.request.user).testID
#         queryset = Question.objects.filter(testID=testID)
#         return queryset