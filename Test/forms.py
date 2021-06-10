# from django import forms
# from .models import TestTaker , Question,TestPackage
# from django.contrib.auth.forms import AuthenticationForm

# class AnswerForm(forms.Form):
#     answer =forms.ChoiceField(choices=(("",""),), widget=forms.RadioSelect())

# class CreateSessionForm(forms.ModelForm):
#     class Meta:
#         model = TestTaker
#         fields = ['testTakerName','testTakerGroup','session_password',]
#         widgets = {
#             'session_password' : forms.PasswordInput()
#         }

# class CreateTestForm(forms.ModelForm):
#     class Meta:
#         model = TestPackage
#         fields = ['testTitle','testAuthor','testSchedule','timeLimit',
#         'passwordTest']
#         widgets = {
#             'passwordTest' : forms.PasswordInput(),
#             'testSchedule' : forms.DateTimeInput(),
#         }
# class AuthTestForm1(forms.Form):
#     codeTest = forms.CharField()

# class AuthTestForm2(forms.Form):
#     passw = forms.CharField(widget=forms.PasswordInput)
    
# class ResumeTestForm(forms.Form):
#     username = forms.CharField(widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': '', 'id': 'session_key'}))
#     password = forms.CharField(widget=forms.PasswordInput(
#         attrs={
#             'class': 'form-control',
#             'placeholder': '',
#             'id': 'password',
#         }
# ))
