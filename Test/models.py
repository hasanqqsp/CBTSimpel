import os
from django.db import models , IntegrityError
from binascii import hexlify
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login
import uuid
import random
import string
import datetime
from utils.generate_id import generate_id,generate_numeric_code
import json

class TestPackage(models.Model):
    defaultSettings = '''{
    "completeRequired": true,
    "randomSequences": true,
    "viewScore": true,
    "viewDetail": true,
    "viewAnswerKey": true,
    "limitByScheduleStart": true,
    "limitByScheduleFinish": false,
    "onlyRegistered": false,
    "canViewScorePage": true,
    "canViewScorePageAuth": false
}'''
    testID = models.CharField(max_length=16, unique=True,editable=True,blank=True)
    testTitle = models.CharField(max_length=1024)
    testAuthor = models.CharField(max_length=1024)
    testCode = models.CharField(default=None, editable=True, max_length=6)
    testSchedule = models.DateField()
    timeLimit = models.IntegerField(default=0, null=True)
    passwordAdminTest = models.CharField(max_length=16,default=None, null=True)
    passwordTest = models.CharField(max_length=16, default="123456")
    welcomeMessage = models.TextField()
    settings = models.JSONField(default=dict(json.loads(defaultSettings)) ,blank=True,null=True)
    def save(self, *args, **kwargs):
        if not self.testID:
            self.testID = generate_id(TestPackage,'testID',16)
        try :
            user = User.objects.get(username=self.testCode)
            group = Group.objects.get(name='testAuthor') 
            group.user_set.add(user)
            user.set_password = str(self.passwordAdminTest)
            user.save()
        except:
            user = User.objects.create_user(self.testCode, '', self.passwordAdminTest)
            user.save()
        super().save(*args, **kwargs)

    def get_question_count(self):
        return self.question_set.all().count()
    def get_random_sequence(self):
        list = []
        while len(list) < self.question_set.all().count():
            r = random.randint(0,self.question_set.all().count()-1)
            if r not in list :
                list.append(r)
        return list
    
    def get_all_question(self,*args):
        list = []
        for i in json.loads(args[0]):
            list.append(self.question_set.all()[i])
        return list

    def get_one_question(self,num,*args):
        if len(args) > 0:
            num = json.loads(args[0])[num-1]
        else:
            num -= 1
        return self.question_set.all()[num]
        
    def __str__(self):
        return f"{self.testID}_{self.testTitle}"
'''
from Test.models import *
all = TestPackage.objects.all()
a1=all[1]
a1.get_one_question(1,a1.get_random_sequence())
'''


class TestTaker(models.Model):
    testTakerID = models.CharField(max_length=16, unique=True,editable=True)
    session_code = models.CharField(max_length=16, unique=True, editable=True)
    session_password = models.CharField(max_length=16)
    testPackage = models.ForeignKey(TestPackage,on_delete=models.CASCADE)
    testTakerName = models.CharField(max_length=128)
    testTakerGroup = models.CharField(max_length=128 ,blank=True ,null=True)
    scoreObtained = models.IntegerField(default=0)
    lastAnswered = models.IntegerField(default=0, editable=True)
    timeStart = models.DateTimeField(auto_now_add=False,editable=True, null=True,blank=True,default=datetime.datetime.now())
    timeFinish = models.DateTimeField(auto_now_add=False,editable=True, null=True,blank=True,default=datetime.datetime.now())
    sequences = models.JSONField(blank=True,null=True)
    def save(self,*args, **kwargs):
        if not self.session_code:
            session_code = generate_numeric_code(TestTaker,'session_code',10)
            user = User.objects.create_user(session_code, None, self.session_password)
            self.session_code = session_code
            user.save()
        if not self.testTakerID:
            self.testTakerID = generate_id(TestTaker,'testTakerID',16)
        if not self.sequences:
            self.sequences = json.dumps(self.testPackage.get_random_sequence())
            
        super().save(*args, **kwargs)
    def timerStart(self):
        self.timeStart = datetime.datetime.now()
        super().save()
        
    def timerEnd(self):
        self.timeFinish = datetime.datetime.now()
        user = User.objects.get(username = self.session_code)
        user.delete()
        super().save()

    def get_all_answer(self):
        list = []
        for i in json.loads(self.sequences):
            q_question = self.testPackage.get_all_question(self.sequences)[i]
            if self.answer_set.filter(question = q_question).exists():
                list.append(self.answer_set.filter(question = q_question)[0])
        return list

    def get_last_answered(self):
        if self.answer_set.all().exists():
            return self.answer_set.all().order_by('timestamp')[0].question 
        else:
            return self.testPackage.get_one_question(1,self.sequences)

    def __str__(self):
        return "{}".format(self.testTakerName)

class Question(models.Model):
    questID = models.CharField(max_length=16, unique = True, blank=True,editable=True)
    question = models.TextField()
    testPackage = models.ForeignKey(TestPackage,on_delete=models.CASCADE)
    choices = models.JSONField(blank=True,null=True)
    answerKey = models.CharField(max_length=1024,default=None, blank=True, null=True)
    trueScore = models.FloatField(default=0)
    defaultScore = models.FloatField(default=0)
    falseScore = models.FloatField(default=0)
    def save(self,*args, **kwargs):
        if not self.questID:
            self.questID = generate_id(Question,'questID',16)
        super().save(*args, **kwargs)
    # def save(self,*args, **kwargs):
    #     sameData = Question.objects.filter(testID=self.testID, questionNum=self.questionNum)
    #     for i in sameData:
    #         if i.id != self.id:
    #             i.delete()
    #         else:
    #             pass
    #     max_score = 0
    #     for i in Question.objects.filter(testID=self.testID):
    #         max_score += i.trueScore
    #     findPack.maxScore = max_score
    #     super().save(*args, **kwargs)
    def get_question_num(self,*args):
        q_question = list(Question.objects.filter(testPackage=self.testPackage))
        sequence = json.loads(args[0])
        inIndex = q_question.index(self)
        inSequence = sequence.index(inIndex)
        return inSequence + 1
    def get_next_question(self,*args):
        q_question = list(Question.objects.filter(testPackage=self.testPackage))
        sequence = json.loads(args[0])
        inIndex = q_question.index(self)
        inSequence = sequence.index(inIndex)
        if inSequence  == len(sequence)-1:
            return None
        num = sequence[inSequence+1]
        return q_question[num]


    def get_prev_question(self,*args):
        q_question = list(Question.objects.filter(testPackage=self.testPackage))
        sequence = json.loads(args[0])
        inIndex = q_question.index(self)
        inSequence = sequence.index(inIndex)
        if inSequence  == 0:
            return None
        num = sequence[inSequence-1]
        return q_question[num]
    '''
from Test.models import *
q= Question.objects.filter(questID='dhfDPn3i6jTA3CnG')[0]
q.get_next_question("[4, 3, 2, 0, 1]").get_prev_question("[4, 3, 2, 0, 1]")
    '''

    def delete(self,*args,**kwargs):
        questionList = Question.objects.filter(testID = self.testID)
        questionCount = questionList.count()
        if not self.questionNum == questionCount:
            print(self.questionNum)
            questionList = questionList[self.questionNum-1:]
            for i in questionList:
                i.questionNum -= 1
                i.save()
                
        super().delete()

    def __str__(self):
        return "{}_{}".format(self.testPackage.testID,self.question)

class Answer(models.Model):
    answerID =  models.CharField(max_length=16, unique=True,editable=True,blank=True)
    testTaker = models.ForeignKey(TestTaker,on_delete=models.CASCADE,related_name='answer_set')
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='answer_set')
    answer = models.CharField(max_length=4096,null=True, blank= True )
    isTrue = models.BooleanField(default=None,null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.answerID:
            self.answerID = generate_id(Answer,'answerID',16)
        super(Answer, self).save(*args, **kwargs)
    # def save(self, *args, **kwargs):
    #     if not self.pk and self.questi == 1:
    #         findTaker = TestTaker.objects.get(testTakerID=self.testTakerID, session_code=self.session_code)
    #         findTaker.startTime = datetime.datetime.now()
    #         findTaker.save()
    #         super(Answer, self).save(*args, **kwargs)
    #     try:
    #         findQuest = Answer.objects.get(questionID=self.questionID, testTakerID=self.testTakerID)
    #     except:
    #         pass
    #     try:
    #         findAnswer = Answer.objects.filter(testTakerID=self.testTakerID, session_code=self.session_code)
    #         findTaker = TestTaker.objects.get(testTakerID= self.testTakerID)

    #         score_obtained = 0
    #         for i in findAnswer:
    #             score_obtained += i.scoreObtain

    #         findTaker.scoreObtained = score_obtained
    #         findTaker.save()

    #         checkAnswer = Question.objects.get(questID=self.questionID,testTakerID=self.testTakerID)
    #         findTaker.lastAnswered = checkAnswer.questionNum
    #         findTaker.save()
    #         if str(self.answer) == str(checkAnswer.answerKey):
    #             self.scoreObtain = checkAnswer.trueScore
    #         else :
    #             self.scoreObtain = checkAnswer.falseScore
    #         checkAnswer.save()

    #         findTaker = Answer.objects.filter(testTakerID==self.testTakerID, session_code=self.session_code)
    #         findTestTaker = TestTaker.objects.get(testTakerID=self.testTakerID)
    #         if self.questi == 1:
    #             findTestTaker.firstAnswerID = self.answerID
    #             findTestTaker.save()
    #         else:
    #             pass

    #         findPA = Answer.objects.get(questionID=self.questionID, testTakerID=self.testTakerID, questi=(self.questi-1))
    #         self.prevAnswerID = findPA.answerID
    #         findPA.nextQuestID = self.answerID
    #         findPA.save()
    #     except:
    #         pass

    #     sameData = Answer.objects.filter(session_code=self.session_code, testID=self.testID, questionID=self.questionID)
    #     for i in sameData:
    #         if i.id != self.id:
    #             i.delete()
    #         else:
    #             pass
    #     super(Answer, self).save(*args, **kwargs)

    # def __str__(self):
    #     return "{} for {}".format(self.testTakerID , self.questionID)
