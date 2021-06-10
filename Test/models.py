import os
from django.db import models , IntegrityError
from binascii import hexlify
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login
import uuid
import random
import string
import datetime
from utils.generate_id import generate_id


class TestPackage(models.Model):
    testID = models.CharField(max_length=16, unique=True,editable=True)
    testTitle = models.CharField(max_length=1024)
    testAuthor = models.CharField(max_length=1024)
    testCode = models.CharField(default=None, editable=True, max_length=6)
    testSchedule = models.DateField()
    timeLimit = models.IntegerField(default=0, null=True)
    passwordAdminTest = models.CharField(max_length=16,default=None, null=True)
    passwordTest = models.CharField(max_length=16, default="123456")
    maxScore = models.IntegerField(default=0)
    welcomeMessage = models.TextField()
    settings = models.JSONField(blank=True,null=True)
    # def __str__(self):
    #     return "{}_{}".format(self.testID,self.testTitle)
    def save(self, *args, **kwargs):
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

    def save(self,*args, **kwargs):
        try :
            User.objects.get(username=self.session_code)
        except:
            user = User.objects.create_user(self.session_code, None, self.session_password)
            user.save()
        super().save(*args, **kwargs)

    # def __str__(self):
    #     return "{}({})".format(self.testTakerID,self.testTakerName)

class Question(models.Model):
    questID = models.CharField(max_length=16, unique = True, editable=True)
    questionNum = models.IntegerField(default=0)
    question = models.TextField()
    testPackage = models.ForeignKey(TestPackage,on_delete=models.CASCADE)
    choices = models.JSONField()
    answerKey = models.CharField(max_length=1024,default=None, blank=True, null=True)
    trueScore = models.FloatField(default=0)
    defaultScore = models.FloatField(default=0)
    falseScore = models.FloatField(default=0)

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

    # def __str__(self):
    #     return "{}.{}_{}".format(self.questionNum,self.testID,self.question)

class Answer(models.Model):
    answerID = models.CharField(max_length=16, default=generate_id , editable=True)
    testTaker = models.ForeignKey(TestTaker,on_delete=models.CASCADE ,max_length=16)
    session_code = models.CharField(max_length=16)
    testID = models.CharField(max_length=16)
    question = models.CharField(max_length=16)
    answer = models.CharField(max_length=4096,null=True, blank= True )
    isTrue = models.BooleanField(default=None,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.pk and self.questi == 1:
            findTaker = TestTaker.objects.get(testTakerID=self.testTakerID, session_code=self.session_code)
            findTaker.startTime = datetime.datetime.now()
            findTaker.save()
            super(Answer, self).save(*args, **kwargs)
        try:
            findQuest = Answer.objects.get(questionID=self.questionID, testTakerID=self.testTakerID)
        except:
            pass
        try:
            findAnswer = Answer.objects.filter(testTakerID=self.testTakerID, session_code=self.session_code)
            findTaker = TestTaker.objects.get(testTakerID= self.testTakerID)

            score_obtained = 0
            for i in findAnswer:
                score_obtained += i.scoreObtain

            findTaker.scoreObtained = score_obtained
            findTaker.save()

            checkAnswer = Question.objects.get(questID=self.questionID,testTakerID=self.testTakerID)
            findTaker.lastAnswered = checkAnswer.questionNum
            findTaker.save()
            if str(self.answer) == str(checkAnswer.answerKey):
                self.scoreObtain = checkAnswer.trueScore
            else :
                self.scoreObtain = checkAnswer.falseScore
            checkAnswer.save()

            findTaker = Answer.objects.filter(testTakerID==self.testTakerID, session_code=self.session_code)
            findTestTaker = TestTaker.objects.get(testTakerID=self.testTakerID)
            if self.questi == 1:
                findTestTaker.firstAnswerID = self.answerID
                findTestTaker.save()
            else:
                pass

            findPA = Answer.objects.get(questionID=self.questionID, testTakerID=self.testTakerID, questi=(self.questi-1))
            self.prevAnswerID = findPA.answerID
            findPA.nextQuestID = self.answerID
            findPA.save()
        except:
            pass

        sameData = Answer.objects.filter(session_code=self.session_code, testID=self.testID, questionID=self.questionID)
        for i in sameData:
            if i.id != self.id:
                i.delete()
            else:
                pass
        super(Answer, self).save(*args, **kwargs)

    def __str__(self):
        return "{} for {}".format(self.testTakerID , self.questionID)
