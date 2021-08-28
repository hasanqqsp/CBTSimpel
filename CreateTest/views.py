from django.shortcuts import render,get_object_or_404
from django import forms
from django.views.generic.base import RedirectView
from django.views.generic.detail import SingleObjectMixin

from CreateTest.forms import (
    CreateTestForm, WelcomePageForm,
    BasicConfigTestForm,CreateTestTakerForm,
    AdvanceConfigTestForm)
from Test.forms import LoginForm 
# from django.views.generic.edit import UpdateView 
from Test.models import (Question , TestPackage, Answer, TestTaker)
from django.urls import reverse, reverse_lazy
from django.http import (HttpResponseRedirect ,JsonResponse,HttpResponse)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
# from django.core import serializers
from django.core.exceptions import ValidationError, PermissionDenied
# from django.utils.translation import gettext as _
from django.contrib.auth.views import LoginView , LogoutView
# from django_quill.forms import QuillFormField
import random ,string, sys , datetime
from django.views.generic import ListView, UpdateView, DetailView, FormView, CreateView,TemplateView
from django.views.generic.edit import DeleteView, FormMixin
from utils.authorization import GroupRequiredMixin,isAdmin,admin_required
from utils.generate_id import generate_id
from utils.mapper import serializeTestTaker
import json
import math
from django.db.models.functions import Lower
from django.db.models import Q
import xlwt 


def index(request):
    return render(request,'CreateTest/index.html')

class NewTest(FormView):
    template_name = 'CreateTest/newTest.html'
    form_class = CreateTestForm
    success_url = reverse_lazy('create:dashboard')
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            credential = authenticate(
                request,
                username=form.cleaned_data['testCode'],
                password=form.cleaned_data['passwordAdminTest']
                )
            login(request,credential)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

def authorLogin(request):
    if (isAdmin(request)):
        return HttpResponseRedirect(reverse("create:dashboard"))

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
                    return HttpResponseRedirect(reverse("create:dashboard"))
            except:
                loginForm.add_error(error=ValidationError(''),field='username')
                    
    else :
        loginForm = LoginForm
    context = {
        'form' : loginForm
    }
    return render(request,'CreateTest/adminLogin.html',context)

@admin_required()
def dashboard(request):
    q_testPackage = TestPackage.objects.get(testCode=request.user) 
    context = {
        'q_testPackage': q_testPackage,
    }
    return render(request,'CreateTest/dashboard.html', context)

class AdvanceConfigView(GroupRequiredMixin,FormView):
    form_class = AdvanceConfigTestForm
    template_name = 'CreateTest/testAdvanceConfig.html'
    success_url = reverse_lazy('create:advanceConfig')
    def form_valid(self, form):
        obj = self.get_object()
        obj.settings = form.cleaned_data
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self,queryset=None):
        return TestPackage.objects.filter(testCode = self.request.user)[0]
        
    def get_initial(self):
        return TestPackage.objects.filter(testCode = self.request.user)[0].settings
    

class BasicConfigView(GroupRequiredMixin,UpdateView):
    model = TestPackage
    form_class = BasicConfigTestForm
    template_name = 'CreateTest/testBasicConfig.html'
    success_url = reverse_lazy('create:basicConfig')
    def get_object(self):
        return TestPackage.objects.filter(testCode=self.request.user)[0]

class QuestionDelete(GroupRequiredMixin,DeleteView):
    
    success_url = reverse_lazy("create:questions")
    def get_object(self):
        return Question.objects.filter(questID = self.kwargs.get('questID'))[0]

class QuestionEdit(GroupRequiredMixin,UpdateView):
    template_name = 'CreateTest/questionEdit.html'
    model = Question
    fields = ['question','answerKey','choices','trueScore','falseScore','defaultScore']

    def get_context_data(self, **kwargs):
        context = super(QuestionEdit, self).get_context_data(**kwargs)
        q_testPackage = TestPackage.objects.filter(testCode=self.request.user)[0]
        extra_context = {
            "questID" : self.kwargs.get('questID'),
            "questionsList" : list(
                self.model.objects.filter(testPackage=q_testPackage)
                                .values('questID')
                ),
            "choices" : json.dumps(context["object"].choices)
        }
        context.update(extra_context)
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        self.object = form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy(
            'create:questionEdit',
            kwargs={
                'questID' : self.get_context_data()['object'].questID
            }
        )

    def get_object(self):
        return Question.objects.filter(questID = self.kwargs.get('questID'))[0]

class QuestionCreate(GroupRequiredMixin,RedirectView):
    def get_redirect_url(self):
        questID = generate_id(Question,'questID',16)
        q_testPackage = TestPackage.objects.filter(testCode=self.request.user)[0]
        Question.objects.create(questID=questID,testPackage=q_testPackage)
        return reverse_lazy('create:questionEdit',kwargs={'questID':questID})

class QuestionsList(GroupRequiredMixin,ListView):
    model = Question    
    template_name = 'CreateTest/questionsList.html'

    def get_queryset(self):
        q_testPackage = TestPackage.objects.filter(testCode = self.request.user)[0]
        qs = self.model.objects.filter(testPackage=q_testPackage)
        return qs

class WelcomePageEdit(UpdateView,GroupRequiredMixin):
    form_class = WelcomePageForm
    model = TestPackage
    template_name = 'CreateTest/welcomePage.html'
    success_url = reverse_lazy("create:welcomePageEdit")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        welcomeMessage = TestPackage.objects.filter(testCode=self.request.user)[0].welcomeMessage
        print(welcomeMessage)
        if welcomeMessage :
            context["welcomeMessage"] = TestPackage.objects.filter(testCode=self.request.user)[0].welcomeMessage
                
        return context
    def get_object(self ,queryset=None):
        obj = self.model.objects.get(testCode=self.request.user)
        return obj

class TestTakerList(GroupRequiredMixin,ListView,FormMixin):
    template_name = 'CreateTest/testTakerList.html'
    paginate_by = 10
    allow_empty = True
    form_class = CreateTestTakerForm
    success_url = reverse_lazy('create:testTakerList')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        q_testTaker = TestTaker.objects.create(
                testTakerName = form.cleaned_data['testTakerName'],
                testTakerGroup = form.cleaned_data['testTakerGroup'],
                session_password = form.cleaned_data['session_password'],
                testPackage = TestPackage.objects.get(testCode=self.request.user)
            )
        q_testTaker.set_time_limit()
        return HttpResponseRedirect(self.get_success_url())

    def get_queryset(self):
        q_testPackage = TestPackage.objects.get(testCode=self.request.user)
        queryset = TestTaker.objects.filter(testPackage=q_testPackage)
        return queryset


    def form_invalid(self, form):
        self.object_list = self.get_queryset()
        return self.render_to_response(self.get_context_data(form=form))

    def get(self, request, *args, **kwargs):
            
        if self.request.GET.get('api'):
            schema = ['session_code','testTakerName','testTakerGroup']
            page = int(request.GET.get('page'))
            qs = self.get_queryset()
            qs_total = qs.count()
            page_size = self.get_paginate_by(qs)
            limit = math.ceil(qs_total / page_size)
            order = request.GET.get('order')
            search = request.GET.get('search')
            if search :
                qs = qs.filter(
                    Q(session_code__icontains=search) | Q(testTakerName__icontains=search) | Q(testTakerGroup__icontains=search)
                    )
            if order:
                strip = '-' if order.startswith('-') else None
                if strip : order = order[1:]
                qs = qs.order_by(Lower(order))
                qs = qs.reverse() if strip else qs
            if page > limit:
               return JsonResponse({
                "total" : 0,
                "data" : [],
                "page" : request.GET.get('page')
                })
            if page_size:
                paginated_qs = self.paginate_queryset(qs, page_size)
            
            response = {
                "total" : qs.count(),
                "data" : list(map(serializeTestTaker,paginated_qs[2])),
                "page" : paginated_qs[1].number
            }
            return JsonResponse(response)

        return super(TestTakerList,self).get(request, *args, **kwargs)

class TestTakerDelete(GroupRequiredMixin,DeleteView):
    success_url = reverse_lazy('create:testTakerList')
    def get_object(self):
        testTakerID = self.kwargs.get('testTakerID')
        return TestTaker.objects.filter(testTakerID = testTakerID)
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.success_url)
  
class AuthorLogout(LogoutView):
    next_page = reverse_lazy('create:login')

class ExportImport(GroupRequiredMixin,TemplateView):
    template_name = 'CreateTest/exportImport.html'

@admin_required()
def exportTestTakerXls(request):
    testCode = request.user
    q_testPackage = TestPackage.objects.filter(testCode=request.user)[0]
    filename = f"{testCode} - {q_testPackage.testTitle}"
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f"attachment; filename={filename}.xls"

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Test Taker')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    schema = ['session_code','testTakerName','testTakerGroup','session_password','scoreObtained','timeStart','timeFinish']
    columns = ['Session Code', 'Test Taker Name', 'Test Taker Group', 'Session Password','Score','Time Start', 'Time Finish']
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = list(TestTaker.objects.filter(testPackage= q_testPackage).values_list(*schema))
    print(rows)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)
    # return HttpResponse('OK')
    return response