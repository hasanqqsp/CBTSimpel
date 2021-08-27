from django import forms
from Test.models import TestPackage, TestTaker
from utils.generate_id import generate_numeric_code
from tempus_dominus.widgets import DateTimePicker
from django.core.exceptions import ValidationError

class CreateTestForm(forms.ModelForm):
    def clean_testCode(self):
        code = self.cleaned_data['testCode']
        if not code:
            return generate_numeric_code(TestPackage,'testCode',6)
        if TestPackage.objects.filter(testCode=code).exists():
            raise ValidationError("testCode can't be used")
        return code

    class Meta:
        model = TestPackage
        fields = ['testTitle','testAuthor','testCode','testScheduleOpen','testScheduleClose','timeLimit','passwordAdminTest','passwordTest']

    testScheduleOpen = forms.DateTimeField(
        input_formats=['%m/%d/%Y %H:%M'],
        widget=DateTimePicker(
            options={
                'sideBySide': True
            },
            attrs={
                'append': 'bi bi-calendar3',
                'icon_toggle': forms.CheckboxInput()
            }
        )
    )
    testScheduleClose = forms.DateTimeField(
        input_formats=['%m/%d/%Y %H:%M'],
        widget=DateTimePicker(
            options={
                'sideBySide': True
            },
            attrs={
                'append': 'bi bi-calendar3',
                'icon_toggle': True
            }
        )
    )



    def __init__(self, *args, **kwargs):
        super(CreateTestForm, self).__init__(*args, **kwargs)
        self.fields['testScheduleOpen'].required = False
        self.fields['testScheduleClose'].required = False
        self.fields['timeLimit'].required = False
        self.fields['testCode'].required = False
        self.fields['passwordTest'].required = False
        self.fields['passwordTest'].widget = forms.PasswordInput(render_value = True)
        self.fields['passwordAdminTest'].widget = forms.PasswordInput()

class BasicConfigTestForm(forms.ModelForm):
    
    class Meta:
        model = TestPackage
        fields = ['testTitle','testAuthor','testCode','testScheduleOpen','testScheduleClose','timeLimit','passwordAdminTest','passwordTest']

    testScheduleOpen = forms.DateTimeField(
        input_formats=['%m/%d/%Y %H:%M'],
        widget=DateTimePicker(
            options={
                'sideBySide': True
            },
            attrs={
                'append': 'bi bi-calendar3',
                'icon_toggle': True
            }
        )
    )
    testScheduleClose = forms.DateTimeField(
        input_formats=['%m/%d/%Y %H:%M'],
        widget=DateTimePicker(
            options={
                'sideBySide': True
            },
            attrs={
                'append': 'bi bi-calendar3',
                'icon_toggle': forms.CheckboxInput()
            }
        )
    )

    passwordAdminTest = forms.PasswordInput(render_value=True)
    passwordTest = forms.PasswordInput(render_value=True)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['testScheduleOpen'].required = False
        self.fields['testScheduleClose'].required = False
        self.fields['timeLimit'].required = False
        self.fields['testCode'].required = False
        self.fields['passwordTest'].required = False
        self.fields['passwordTest'].widget = forms.PasswordInput(render_value = True)
        self.fields['passwordAdminTest'].widget = forms.PasswordInput()

class WelcomePageForm(forms.ModelForm):
    class Meta:
        model = TestPackage
        fields = ["welcomeMessage"]

class QuestionForm(forms.Form):
    question = forms.CharField(widget=forms.Textarea)
    trueScore = forms.FloatField()
    def __init__(self,*args,**kwargs):
        super().__init__()


class AdvanceConfigTestForm(forms.Form):
    question = forms.CharField(widget=forms.Textarea)
    trueScore = forms.FloatField()
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

class CreateTestTakerForm(forms.ModelForm):
    class Meta:
        model = TestTaker
        fields = ['session_code','testTakerName','testTakerGroup','session_password',]
        widgets = {
            'session_password' : forms.PasswordInput()
        }

    def clean_session_code(self):
        data = self.cleaned_data["session_code"]
        qs = TestTaker.objects.filter(session_code=data)
        if qs.exists():
            raise ValidationError('SESSION CODE NOT AVAILABLE')
        return data

class AdvanceConfigTestForm(forms.Form):
    isActive = forms.BooleanField(widget=forms.CheckboxInput,required=False)
    completeRequired = forms.BooleanField(widget=forms.CheckboxInput,required=False)
    randomSequences = forms.BooleanField(widget=forms.CheckboxInput,required=False)
    viewScore = forms.BooleanField(widget=forms.CheckboxInput,required=False)
    viewAnswerKey = forms.BooleanField(widget=forms.CheckboxInput,required=False)
    limitByScheduleStart = forms.BooleanField(widget=forms.CheckboxInput,required=False)
    limitByScheduleFinish = forms.BooleanField(widget=forms.CheckboxInput,required=False)
    onlyRegistered = forms.BooleanField(widget=forms.CheckboxInput,required=False)
    canViewScorePage = forms.BooleanField(widget=forms.CheckboxInput,required=False)
    canViewScorePageAuth = forms.BooleanField(widget=forms.CheckboxInput,required=False)
    allowEditData = forms.BooleanField(widget=forms.CheckboxInput,required=False)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)