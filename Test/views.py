from django.shortcuts import render,get_object_or_404
from .models import (Question , TestPackage, Answer, TestTaker)
from .forms import *
from django.http import (HttpResponseRedirect ,HttpResponse,HttpResponseNotFound)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.utils import timezone
import datetime



def index(request):
    return render(request, 'Test/index.html')

def showTest(request):
    testPackage = TestPackage.objects.all() 
    context = {
        'TestPackage' : testPackage,
    }
    return render(request, 'Test/test.html',context)

def joinTest(request):
    form = AuthTestForm1()
    if request.method == 'POST':
        form = AuthTestForm1(request.POST or None)
        if form.is_valid():
            testCode = request.POST.get('testCode')
            try:
                query = TestPackage.objects.get(testCode=testCode,settings__isActive = True)
                if query.settings['onlyRegistered']:
                    return HttpResponseRedirect('/test/resume')
                return HttpResponseRedirect('/test/{}'.format(query.testID))
            except :
                form.add_error(error=ValidationError(''),field='testCode')


    context = {
        'form' : form
    }
    return render(request, 'Test/joinTest.html',context)

@login_required(login_url='/test/resume')            
def changeTest(request,testID,testTakerInfo):
    q_testPackage = TestPackage.objects.get(testID=testID)
    if request.user.is_authenticated :
        q_testTaker = TestTaker.objects.get(session_code = request.user)
    else :
        return HttpResponseRedirect('/test/createsession/{}'.format(testID))
        
    context = {
        "savedTest" : TestPackage.objects.get(testID=q_testTaker.testPackage.testID),
        "redirID" : testID,
        'testInfo': q_testPackage,
        'testTakerInfo': q_testTaker
    }
    return render(request, 'Test/changeTest.html',context)

def detailTest(request, testID):
    if testID == 'createsession':
        return HttpResponseRedirect(reverse('test:createSession', kwargs={'testID':'404'}))
    if testID == 'sessioninfo':
        return HttpResponseRedirect(reverse('test:sessionInfo'))

    q_testPackage = TestPackage.objects.get(testID=testID)
    q_testTaker = TestTaker.objects.filter(session_code = request.user) 

    if q_testTaker.exists() and q_testPackage != q_testTaker[0].testPackage:
        return changeTest(request,testID,q_testTaker)
    elif q_testTaker.exists():
        return HttpResponseRedirect('/test/resume')    

    form = AuthTestForm2(request.POST or None)
    if q_testPackage.passwordTest == 'None':
        form = None
        if request.method == 'POST':
            return HttpResponseRedirect(f"/test/createsession/{testID}") 
    else :
        if request.method == 'POST':
            form = AuthTestForm2(request.POST or None)
            if form.is_valid():
                password = request.POST.get('password')
                if str(password) == str(q_testPackage.passwordTest):
                    return HttpResponseRedirect(reverse('test:createSession', kwargs={'testID':testID}))
                else:
                    form.add_error(error=ValidationError(''),field='password')
        
    context = {
            'form' : form,
            'q_testPackage': q_testPackage,
            'timeNow' : timezone.now()
        
    }
    return render(request, 'Test/overviewTest.html', context)
        
@login_required(login_url='/test/resume')  
def welcomeTest(request,testID):
    if not TestTaker.objects.filter(session_code = request.user).exists():
        pass
    q_testTaker = TestTaker.objects.get(session_code= request.user)                # session[0]
    q_testPackage = TestPackage.objects.get(testID=testID)

    if request.method == 'POST':
        if not q_testTaker.timeStart:
            q_testTaker.timerStart()
        return HttpResponseRedirect("{}".format(q_testPackage.get_one_question(1,q_testTaker.sequences).questID))
    context = {
        'title' : q_testPackage.testTitle,
        'quest' : q_testPackage,
        'welcomeMessage' : q_testPackage.welcomeMessage,
        'now' : timezone.now()
    }
    return render(request,'Test/welcomeTest.html',context)

@login_required(login_url='/test/resume')  
def verifyAnswer(request, testID):
    q_testPackage = TestPackage.objects.filter(testID=testID)
    if len(q_testPackage) > 0:
        q_testPackage = q_testPackage[0]
    else:
        return HttpResponseNotFound()

    q_testTaker = TestTaker.objects.filter(session_code=request.user) 

    if len(q_testTaker) > 0:
        q_testTaker = q_testTaker[0]
    else:
        return HttpResponseRedirect('/test/resume')
        
    q_last_answered_quest = q_testTaker.get_last_answered()
    q_answer = q_testTaker.get_all_answer()
    q_question = q_testPackage.get_all_question(q_testTaker.sequences)
    
    

    if request.method == "POST":
        q_testTaker.timerEnd()
        if q_testPackage.settings["canViewScorePage"]:
            return HttpResponseRedirect('/test/viewscore/{}'.format(q_testTaker.session_code))
                  
        return HttpResponseRedirect ('../../join')

    context = {
        'takerQuery' : q_testTaker,
        'packQuery' : q_testPackage,
        'answerQuery' : q_answer,
        'questQuery' : q_question,
        
        'timeNow' : timezone.now(),
        'lastQuest' : q_last_answered_quest.questID,
        'questionCount' : q_testPackage.get_question_count(),
        'query' : q_testTaker.get_all_answer_and_question(),
    }

    return render(request, 'Test/verifyAnswer.html',context)

@login_required(login_url='/test/resume')  
def doTest(request, testID, questID):
    q_testPackage = TestPackage.objects.get(testID=testID)
    q_question = q_testPackage.question_set.get(questID=questID)
    q_testTaker = TestTaker.objects.get(session_code = request.user)
    try:
        q_testTaker = TestTaker.objects.get(session_code = request.user)
    except:
        return HttpResponseRedirect('/test/resume')

    q_answer = q_testTaker.answer_set.filter(question=q_question)

    if Question.objects.get(questID=questID).get_next_question(q_testTaker.sequences) == None:
        query = "verify"
    else: 
        # if next question not found 
        query = q_question.get_next_question(q_testTaker.sequences).questID
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if len(q_answer) > 0:
            q_answer[0].delete()
        if request.POST['is_timeout']:
            return HttpResponseRedirect('../q/{}'.format('verify'))    
        if form.is_valid():
            Answer.objects.create(
                question = q_question,
                testTaker=q_testTaker,
                answer=request.POST['answer']
            )
            
           
            return HttpResponseRedirect('../q/{}'.format(query))
        else:
            form = AnswerForm
    else:
        if len(q_answer) > 0:
            form = AnswerForm({'answer':q_answer[0].answer})
        else:
            form = AnswerForm
       
    CHOICES = []
    for i in q_question.choices:
        CHOICES.append((i['choiceCode'],i['choiceLabel']))
    
    form.base_fields['answer'].choices = CHOICES

    context = {
        'q_testTaker' : q_testTaker,
        'q_question' : q_question,
        'form' : form,
        'q_testPackage': q_testPackage,
        'timeNow' : timezone.now(),
        'question_list' : q_testPackage.get_all_question(q_testTaker.sequences),
        'next_question' : q_question.get_next_question(q_testTaker.sequences),
        'prev_question' : q_question.get_prev_question(q_testTaker.sequences),
        'indexOf' : q_question.get_question_num(q_testTaker.sequences)
        
    }
    return render(request,'Test/doTest.html',context)

def createSession(request,testID):
    get_object_or_404(TestPackage,testID=testID)
      
    if request.method == 'POST':
        createSessionForm = CreateSessionForm(request.POST or None)
        if createSessionForm.is_valid():
            
            q_testTaker = TestTaker.objects.create(
                testTakerName = request.POST.get('testTakerName'),
                testTakerGroup = request.POST.get('testTakerGroup'),
                session_password = request.POST.get('session_password'),
                testPackage = TestPackage.objects.get(testID=testID)
            )
            q_testTaker.set_time_limit()
            credential = authenticate(request, username=q_testTaker.session_code, password=request.POST.get('session_password'),)
            login(request,credential)
        return HttpResponseRedirect('../{}'.format(testID))
    else :
        createSessionForm = CreateSessionForm
    context = {
        'form' : createSessionForm
    }

    return render(request,'Test/createSession.html',context)

@login_required(login_url='/test/resume')  
def sessionInfo(request):
    q_testTaker = TestTaker.objects.filter(session_code=request.user,timeFinish=None)
    if not TestTaker.objects.filter(session_code=request.user,timeFinish=None).exists:
        return HttpResponseRedirect('/test/resume')
    context = {
        'q_testTaker' : q_testTaker[0], 
        }   
    return render(request,'Test/sessionInfo.html',context)     

def sessionEdit(request):
    q_testTaker = TestTaker.objects.filter(session_code=request.user,timeFinish=None)
    if not TestTaker.objects.filter(session_code=request.user,timeFinish=None).exists:
        return HttpResponseRedirect('/test/resume')
    context = {
        'q_testTaker' : q_testTaker[0], 
        }   
    return render(request,'Test/sessionInfo.html',context)

def resumeTest(request,*args, **kwargs):
    q_testTaker = TestTaker.objects.filter(session_code=request.user or request.POST.get("username"))                           
    
    #print(q_testTaker)
    if request.user.is_authenticated and len(q_testTaker) > 0:
        return HttpResponseRedirect('/test/{}/q/{}'.format(q_testTaker[0].testPackage.testID,  'welcome'))

    else :
        loginForm = ResumeTestForm(request.POST or None)
        if request.method == 'POST':
            loginForm = ResumeTestForm(request.POST or None)
            if loginForm.is_valid():
                loginForm = ResumeTestForm(request.POST)
                credential = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'),)
                
                try:
                    User.objects.get(username=request.POST.get("username"))
                    
                    if credential == None:
                        loginForm.add_error(error=ValidationError(''),field='password')
                    else:
                        login(request,credential)
                        
                        return HttpResponseRedirect('/test/{}/q/{}'.format(q_testTaker.testPackage.testID, 'welcome'))
                except:
                    loginForm.add_error(error=ValidationError(''),field='username')
                        
        else :
            loginForm = ResumeTestForm
    context = {
        'form' : loginForm
    }
    return render(request,'Test/resume.html',context)

@login_required(login_url='/test/resume',redirect_field_name=None)  
def cancelTest(request,redirID):
    q_user = User.objects.get(username = request.user)
    q_user.delete()
    q_testTaker = TestTaker.objects.get(session_code=request.user,)
    q_testTaker.delete()
    if redirID == 'none':
        return HttpResponseRedirect('/test/join')
        
    else:
        return HttpResponseRedirect('/test/{}'.format(redirID))

def viewScore(request, session_code):
    q_testTaker = TestTaker.objects.filter(session_code=session_code) 
    q_testPackage = q_testTaker[0].testPackage
    if len(q_testTaker) > 0 and q_testTaker[0].timeFinish and q_testPackage.settings["canViewScorePage"]:
        q_testTaker = q_testTaker[0]
    else:
        return HttpResponseNotFound()

      
    q_last_answered_quest = q_testTaker.get_last_answered()
    q_answers = q_testTaker.get_all_answer()
    q_question = q_testPackage.get_all_question(q_testTaker.sequences)
   
    context = {
        'q_testTaker' : q_testTaker,
        'q_testPackage' : q_testPackage,
        'q_answer' : q_answers,
        'q_question' : q_question,
    }

    return render(request, 'Test/viewScore.html',context)


# def viewScore(request,session_code):
#     q_testTaker = get_object_or_404(TestTaker, session_code = session_code)
#     answerQuery = Answer.objects.filter(session_code=session_code)
#     packQuery = TestPackage.objects.get(testID=q_testTaker.testID)
#     questQuery = Question.objects.filter(testID=q_testTaker.testID).order_by('questionNum')

#     for i in answerQuery:
#         score_obtained += i.scoreObtain
#     q_testTaker.scoreObtained = score_obtained
#     q_testTaker.save()
#     for i in range(len(questQuery)):
#         try:
#             nth_answer = Answer.objects.get(testID=q_testTaker.testID,session_code=session_code,num_ofAnswer=i+1)
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
#         'takerQuery' : q_testTaker ,
#         'packQuery' : packQuery,
#         'query': query
#     }
#     return render(request,'Test/viewScore.html',context)

def generate_pdf(request, session_code):
    q_testTaker = get_object_or_404(TestTaker, session_code = session_code)
    q_answers = Answer.objects.filter(session_code=session_code)
    q_testPackage = TestPackage.objects.get(testID=q_testTaker.testID)
   
    
    q_testTaker.save()
    context = {
        'q_answers': q_answers,
        'q_testTaker' : q_testTaker ,
        'q_testPackage' : q_testPackage,
    }

    # Rendered
    html_string = render_to_string('Test/viewScore.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_people.pdf'
    response['Content-Transfer-Encoding'] = 'utf-8'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read()) 
    return response