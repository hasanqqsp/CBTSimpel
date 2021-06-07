from django.contrib import admin
from .models import (TestPackage , Question,
Answer, TestTaker, TestWelcome)
# Register your models here.
class TestPackageAdmin(admin.ModelAdmin):
    fields = ['id' ,'testID' ,'testTitle', 'testAuthor',
    'questionCount','testSchedule','passwordTest',
    'testCode', 'firstQuestID', 'maxScore','passwordAdminTest','timeLimit']
    readonly_fields = ['id','questionCount',
    'testCode','firstQuestID','maxScore' ]

class QuestionAdmin(admin.ModelAdmin):
    fields = ['id','questID','questionNum', 'question',
     'testID','nextQuestID','prevQuestID', 
     'answerKey','choiceFirst','choiceSecond',
     'choiceThird','choiceFourth','choiceFifth',
     'choiceSixth','trueScore','falseScore']
    readonly_fields = ['id','questID','nextQuestID','prevQuestID']

class AnswerAdmin(admin.ModelAdmin):
    fields = ['id','answerID','testTakerID','session_key','testID',
    'questionID','num_ofAnswer','answer', 'scoreObtain']
    readonly_fields = ['id'
    ]
class TestTakerAdmin(admin.ModelAdmin):
    fields = ['id','testTakerID','session_key','session_password','testID'
    ,'testTakerName','testTakerGroup',
    'scoreObtained','timeStart']
    readonly_fields = ['id','scoreObtained','testTakerID','session_key']

class TestWelcomeAdmin(admin.ModelAdmin):
    fields=['testID','welcomeMessage']

admin.site.register(TestPackage, TestPackageAdmin )
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(TestTaker,TestTakerAdmin)
admin.site.register(TestWelcome,TestWelcomeAdmin)

