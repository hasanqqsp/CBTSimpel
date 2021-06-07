from Test import models as testModels
from django import forms
from django_quill.forms import QuillFormField


class CreateTestPackage(forms.ModelForm):
    class Meta:
        model = testModels.TestPackage
        fields = ("testTitle","testAuthor","testCode","testSchedule","timeLimit",
            "passwordTest","passwordAdminTest"
        )

class UpdateTestInfo(forms.ModelForm):
    class Meta:
        model = testModels.TestPackage
        fields = ("testTitle","testAuthor","testSchedule","timeLimit","passwordTest","testCode","maxScore","questionCount",
        "passwordAdminTest"
        )
        disabled_fields = ('testCode','maxScore','questionCount')
        def __init__(self, *args, **kwargs):
            super(ItemForm, self).__init__(*args, **kwargs)
            for field in self.disabled_fields:
                self.fields[field].disabled = True

class WelcomeMessage(forms.Form):
    welcomeMessage = QuillFormField()
    def __init__(self,*args,**kwargs):
        super().__init__()


class QuestionForm(forms.Form):
    question = QuillFormField()
    choice1 = QuillFormField()
    choice2 = QuillFormField()
    choice3 = QuillFormField()
    choice4 = QuillFormField()
    choice5 = QuillFormField()
    choice6 = QuillFormField()
    answerKey = forms.ChoiceField(choices=(("",""),), widget=forms.RadioSelect())
    def __init__(self,*args,**kwargs):
        super().__init__()

