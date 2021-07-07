from django import forms
from .models import TestTaker , Question,TestPackage
# from django.contrib.auth.forms import AuthenticationForm

class AnswerForm(forms.Form):
    answer = forms.ChoiceField(choices=(("",""),), widget=forms.RadioSelect(),required=False)


class CreateSessionForm(forms.ModelForm):
    class Meta:
        model = TestTaker
        fields = ['testTakerName','testTakerGroup','session_password',]
        widgets = {
            'session_password' : forms.PasswordInput()
        }

class UpdateSessionForm(forms.ModelForm):
    password_confirm =  forms.CharField(widget=forms.PasswordInput,required=False)
    class Meta:
        model = TestTaker
        fields = ['testTakerName','testTakerGroup','session_password',]
        widgets = {
            'session_password' : forms.PasswordInput()
        }
        required = {
            'session_password' : False
        }

class AuthTestForm1(forms.Form):
    testCode = forms.CharField()

class AuthTestForm2(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    
class ResumeTestForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'session_key'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'password',
        }
))

class FindScoreForm(forms.Form):
    sessionCode = forms.CharField()

class AuthScoreForm(forms.Form):
    session_password = forms.CharField(widget=forms.PasswordInput())