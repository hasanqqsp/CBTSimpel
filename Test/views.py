# from django.shortcuts import render,get_object_or_404
# from .models import (Question , TestPackage, Answer, TestTaker)
# from .forms import (AnswerForm , CreateSessionForm, AuthTestForm2, 
#     AuthTestForm1, CreateTestForm, ResumeTestForm, )
# from django.http import (HttpResponseRedirect ,HttpResponse)
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.forms import AuthenticationForm
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext as _
# from django.contrib.auth.views import LoginView
# from django.core import serializers
# from wkhtmltopdf.views import PDFTemplateResponse
# import datetime
# import pdfkit
# import random 
# import string
# from django.template.loader import render_to_string
# from weasyprint import HTML
# import tempfile



# def index(request):
#     return render(request, 'Test/index.html')

# def showTest(request):
#     testPackage = TestPackage.objects.all() 
#     context = {
#         'TestPackage' : testPackage,
#     }
#     return render(request, 'Test/test.html',context)

# def joinTest(request):
#     form = AuthTestForm1(request.POST or None)
#     if request.method == 'POST':
#         form = AuthTestForm1(request.POST or None)
#         if form.is_valid():
#             codeTest = request.POST.get('codeTest')
#             try:
#                 query = TestPackage.objects.get(testCode=codeTest)
#                 return HttpResponseRedirect('/test/{}'.format(query.testID))
#             except :
#                 form.add_error(error=ValidationError(''),field='codeTest')


#     context = {
#         'form' : form
#     }
#     return render(request, 'Test/joinTest.html',context)
            
# def changeTest(request,idtest,testTakerInfo):
#     querytest = TestPackage.objects.get(testID=idtest)
#     if request.user.is_authenticated:
#         findTestTaker = TestTaker.objects.get(session_key = request.user)
#     else :
#         return HttpResponseRedirect('/test/createsession/{}'.format(idtest))
        
#     context = {
#         "savedTest" : TestPackage.objects.get(testID=findTestTaker.testID),
#         "redirID" : idtest,
#         'testInfo': querytest,
#         'testTakerInfo': testTakerInfo
#     }
#     return render(request, 'Test/changeTest.html',context)

# def detailTest(request, idtest):
#     try : 
#         findTestTaker = TestTaker.objects.get(session_key = request.user) 
#     except : 
#         return HttpResponseRedirect('/test/createsession/{}'.format(idtest))        
#     if idtest == 'join':
#         return joinTest(request)
#     elif idtest != findTestTaker.testID:
#         return changeTest(request,idtest,findTestTaker)

#     else :
#         form = AuthTestForm2(request.POST or None)
#         query = TestPackage.objects.get(testID=idtest)
#         is_noPassword = False
#         if query.passwordTest == 'None':
#             form = None
#         else :
#             if request.method == 'POST':
#                 form = AuthTestForm2(request.POST or None)
#                 if form.is_valid():
#                     passw = request.POST.get('passw')
#                     if str(passw) == str(query.passwordTest):
#                         return HttpResponseRedirect("q/welcome")
#                     else:
#                         form.add_error(error=ValidationError('Terjadi Kesalahan, Password Mungkin Salah'),field='passw')
#         try : 
#             findTestTaker = TestTaker.objects.get(session_key = request.user) 
#         except : 
#             return HttpResponseRedirect('/test/createsession/{}'.format(idtest))

#         context = {
#             'form' : form,
#             'testInfo': query,
#             'testTakerInfo': findTestTaker
#         }
#         return render(request, 'Test/overviewTest.html', context)

# def welcomeTest(request,idtest):
#     findTakerData = TestTaker.objects.get(session_key= request.user)                # session[0]
#     getLastAnsweredQuest = Question.objects.get(testID=findTakerData.testID,questionNum=findTakerData.lastAnswered or 1) # session[2]
#     packQuery = TestPackage.objects.get(testID=idtest)
#     if request.method == 'POST':
#         Answer.objects.create(
#             testID=idtest,
#             session_key = str(request.user),
#             testTakerID=findTakerData.testTakerID,
#             questionID= packQuery.firstQuestID,
#             num_ofAnswer=1,
#             answer=None
#         )
#         return HttpResponseRedirect("{}".format(packQuery.firstQuestID))
#     context = {
#         'title' : packQuery.testTitle,
#         'quest' : packQuery,
#         'welcome' : query,
#         'lastQuest' : getLastAnsweredQuest.questID
#     }
#     return render(request,'Test/welcomeTest.html',context)

# def verifyAnswer(request, idtest):
#     try:
#         takerQuery = TestTaker.objects.get(session_key=request.user, testID=idtest)
#     except:
#         return HttpResponseRedirect('/test/resume')
#     getLastAnsweredQuest = Question.objects.get(testID=takerQuery.testID,questionNum=takerQuery.lastAnswered or 1) # session[2]
#     packQuery = TestPackage.objects.get(testID=idtest)
#     answerQuery = Answer.objects.filter(testID=idtest,session_key=request.user).order_by('num_ofAnswer')
#     questQuery = Question.objects.filter(testID=idtest).order_by('questionNum')
#     query = []
#     for i in range(len(questQuery)):
#         try:
#             i_answer = Answer.objects.get(testID=idtest,session_key=request.user,num_ofAnswer=i+1)
#             i_answer = i_answer.answer
#             print(i_answer)
#         except: 
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
            
#         query.append({'num':'{}'.format(questQuery[i].questionNum),'question':'{}'.format(questQuery[i].question),'answer':"{}".format(answer),'questID':'{}'.format(questQuery[i].questID)})

#     if request.method == "POST":
#         takerQuery.timeFinish = datetime.datetime.now()
#         user = User.objects.get(username = request.user)
#         user.delete()
#         return HttpResponseRedirect ('../../join')
#     context = {
#         'takerQuery' : takerQuery,
#         'packQuery' : packQuery,
#         'answerQuery' : answerQuery,
#         'questQuery' : questQuery,
#         'query' : query,
#         'ob': takerQuery.timeStart,
#         'lastQuest' : getLastAnsweredQuest.questID
#     }

#     return render(request, 'Test/verifyAnswer.html',context)

# def doTest(request, idtest, idquest):
#     querytest = TestPackage.objects.get(testID=idtest)
#     json_serializer = serializers.get_serializer("json")()
#     questionList = Question.objects.filter(testID=idtest)
#     queryset = Question.objects.get(questID=idquest, testID=idtest)
#     try:
#         findTestTaker = TestTaker.objects.get(session_key = request.user)
#     except:
#         return HttpResponseRedirect('/test/resume')

#     json_question = json_serializer.serialize(Question.objects.filter(testID=idtest), ensure_ascii=False)

#     try:
#         findAnswer = Answer.objects.get(session_key=request.user, testID=idtest, questionID=idquest)
#     except:
#         findAnswer = None
#     if Question.objects.get(questID=idquest).nextQuestID == None:
#         query = "verify"
#     else: # if next question not found 
#         query = Question.objects.get(questID=idquest).nextQuestID 
#     if request.method == 'POST':
#         form = AnswerForm(request.POST)
#         print(form.errors)
#         if form.is_valid():
#             user = request.user
#             Answer.objects.create(
#                 testID=idtest,
#                 session_key = str(user),
#                 testTakerID=findTestTaker.testTakerID,
#                 questionID= idquest,
#                 num_ofAnswer=queryset.questionNum,
#                 answer=request.POST['answer'],
#             )
#             print(request.POST['answer'] == queryset.answerKey)

#             return HttpResponseRedirect('../q/{}'.format(query))
#         else:
#             form = AnswerForm
#     else:
#         if findAnswer is not None:
#             form = AnswerForm({'answer':findAnswer.answer})
#         else:
#             form = AnswerForm
#         # form = AnswerForm
#     CHOICES = (
#         ("A",queryset.choiceFirst),
#         ("B" ,queryset.choiceSecond),
#         ("C",queryset.choiceThird),
#         ("D",queryset.choiceFourth),
#         ("E",queryset.choiceFifth),
#         ("F",queryset.choiceSixth),
#     )
#     form.base_fields['answer'].choices = CHOICES
#     context = {
#         'takerQuery' : findTestTaker,
#         'question' : queryset,
#         'form' : form,
#         'json_q': json_question,
#         'testInfo': querytest,
#         'question_list' : questionList,
#     }
#     return render(request,'Test/doTest.html',context)

# def createSession(request,*args, **kwargs):
#     def generate_sessionkey():
#         '''Generate an 10-character Integer'''
#         rand = ''.join([random.choice(string.digits) for n in range(10)])
#         try:
#             # if this possible ID exists, run again:
#             TestTaker.objects.get(session_key=rand)
#             return self.generate_sessionkey()
#         except:
#             return rand
    
#     check = get_object_or_404(TestPackage,testID=kwargs['idtest'])
        
#     if request.method == 'POST':
#         createSessionForm = CreateSessionForm(request.POST or None)
#         if createSessionForm.is_valid():
#             skey = generate_sessionkey()
#             TestTaker.objects.create(
#                 session_key=skey,
#                 testTakerName = request.POST.get('testTakerName'),
#                 testTakerGroup = request.POST.get('testTakerGroup'),
#                 session_password = request.POST.get('session_password'),
#                 testID = kwargs['idtest']
#             )
            
#             credential = authenticate(request, username=skey, password=request.POST.get('session_password'),)
#             login(request,credential)
#         return HttpResponseRedirect('../{}'.format(kwargs['idtest']))
#     else :
#         createSessionForm = CreateSessionForm
#     context = {
#         'form' : createSessionForm
#     }

#     return render(request,'Test/createSession.html',context)

# def resumeTest(request,*args, **kwargs):
#     def getUserSession(request):
#         findTakerData = TestTaker.objects.get(session_key= request.user or request.POST.get("username"))                # session[0]
#         getTestPackage = TestPackage.objects.get(testID=findTakerData.testID)                                           # session[1]
#         getLastAnsweredQuest = Question.objects.get(testID=findTakerData.testID,questionNum=findTakerData.lastAnswered or 1) # session[2]
#         return(findTakerData,getTestPackage,getLastAnsweredQuest)

#     try:
#         session = getUserSession(request)
#     except:
#         session = None
#     if request.user.is_authenticated and session is not None:
#         return HttpResponseRedirect('/test/{}/q/{}'.format(session[0].testID, session[2].questID))

#     else :
#         if request.method == 'POST':
#             loginForm = ResumeTestForm(request.POST or None)
#             if loginForm.is_valid():
#                 loginForm = ResumeTestForm(request.POST)
#                 credential = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'),)
#                 try:
#                     User.objects.get(session_key=request.POST.get("username"))
#                     if credential == None:
#                         loginForm.add_error(error=ValidationError(''),field='password')
#                     else:
#                         login(request,credential)
#                         session = getUserSession(request)
#                         return HttpResponseRedirect('/test/{}/q/{}'.format(session[0].testID, session[2].questID))
#                 except:
#                     loginForm.add_error(error=ValidationError(''),field='username')
                        
#         else :
#             loginForm = ResumeTestForm
#     context = {
#         'form' : loginForm
#     }
#     return render(request,'Test/resume.html',context)

# def cancelTest(request,**kwargs):
#     user = User.objects.get(username = request.user)
#     user.delete()
#     Taker = TestTaker.objects.get(session_key=request.user,)
#     Taker.delete()
#     if kwargs['redirID'] == 'none':
#         return HttpResponseRedirect('/test/join')
        
#     else:
#         return HttpResponseRedirect('/test/{}'.format(kwargs['redirID']))

# def viewScore(request,session_key):
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
#             nth_answer = Answer.objects.get(testID=findTestTaker.testID,session_key=session_key,num_ofAnswer=i+1)
#             i_answer = nth_answer.answer
#             print(i_answer)
#         except: 
#             i_answer = ""
#         print(i_answer)
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
#             'question':'{}'.format(questQuery[i].question),
#             'answer':"{}".format(answer),
#             'questID':'{}'.format(questQuery[i].questID),
#             'score':"{}".format(nth_answer.scoreObtain)})
#     context = {
#         'answerQuery': answerQuery,
#         'takerQuery' : findTestTaker ,
#         'packQuery' : packQuery,
#         'query': query
#     }
#     return render(request,'Test/viewScore.html',context)

# def generate_pdf(request, session_key):
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
#             nth_answer = Answer.objects.get(testID=findTestTaker.testID,session_key=session_key,num_ofAnswer=i+1)
#             i_answer = nth_answer.answer
#             print(i_answer)
#         except: 
#             i_answer = ""
#         print(i_answer)
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
#             'question':'{}'.format(questQuery[i].question),
#             'answer':"{}".format(answer),
#             'questID':'{}'.format(questQuery[i].questID),
#             'score':"{}".format(nth_answer.scoreObtain)})
#     context = {
#         'answerQuery': answerQuery,
#         'takerQuery' : findTestTaker ,
#         'packQuery' : packQuery,
#         'query': query
#     }

#     # Rendered
#     html_string = render_to_string('Test/viewScore.html', context)
#     html = HTML(string=html_string)
#     result = html.write_pdf()

#     # Creating http response
#     response = HttpResponse(content_type='application/pdf;')
#     response['Content-Disposition'] = 'inline; filename=list_people.pdf'
#     response['Content-Transfer-Encoding'] = 'utf-8'
#     with tempfile.NamedTemporaryFile(delete=True) as output:
#         output.write(result)
#         output.flush()
#         output = open(output.name, 'rb')
#         response.write(output.read()) 
#     return response