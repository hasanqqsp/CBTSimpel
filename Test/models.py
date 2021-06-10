import os
from django.db import models , IntegrityError
from binascii import hexlify
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import uuid
import random
import string
import datetime
from utils.generate_id import generate_id


class TestPackage(models.Model):
    testID = models.CharField(max_length=16, unique=True ,editable=True)
    testTitle = models.CharField(max_length=1024)
    testAuthor = models.CharField(max_length=1024)
    questionCount = models.CharField(default=0, max_length=4)
    testCode = models.CharField(default=None, editable=True, max_length=6)
    testSchedule = models.DateField()
    timeLimit = models.IntegerField(default=0, null=True)
    passwordAdminTest = models.CharField(max_length=16,default=None, null=True)
    passwordTest = models.CharField(max_length=16, default="123456")
    firstQuestID = models.CharField(max_length=16, default=None, blank=True, null=True, editable=True)
    welcomeMessageID = models.CharField(max_length=16, default=None, blank=True, null=True, editable=True)
    maxScore = models.IntegerField(default=0)

    def __str__(self):
        return "{}_{}".format(self.testID,self.testTitle)
    def save(self, *args, **kwargs):
        try :
            user = User.objects.get(username=self.testCode)
            user.set_password = str(self.passwordAdminTest)
            user.save()
        except:
            user = User.objects.create_user(self.testCode, '', self.passwordAdminTest)
            user.save()

        super().save(*args, **kwargs)

class Question(models.Model):
    questID = models.CharField(max_length=16, unique = True, editable=True)
    questionNum = models.IntegerField(default=0)
    question = models.TextField()
    testID = models.CharField(max_length=16)
    answerKey = models.CharField(max_length=1024,default=None, blank=True, null=True)
    choiceFirst = models.TextField(default=None, blank=True, null=True)
    choiceSecond = models.TextField(default=None, blank=True, null=True)
    choiceThird = models.TextField(default=None, blank=True, null=True)
    choiceFourth = models.TextField(default=None, blank=True, null=True)
    choiceFifth = models.TextField(default=None, blank=True, null=True)
    choiceSixth = models.TextField(default=None, blank=True, null=True)
    nextQuestID = models.CharField(max_length=16, default=None, blank=True, null=True)
    prevQuestID = models.CharField(max_length=16, default=None, blank=True, null=True)
    trueScore = models.IntegerField(default=0)
    falseScore = models.IntegerField(default=0)
    timeAdd = models.DateTimeField(auto_now_add=True)


    def save(self,*args, **kwargs):
        findPack = TestPackage.objects.get(testID=self.testID)
        if str(self.questionNum) == '1' :
            findPack.firstQuestID = self.questID
        else:
            pass

        findPack.questionCount="{}".format(len(Question.objects.filter(testID=self.testID)))
        findPack.save()
        sameData = Question.objects.filter(testID=self.testID, questionNum=self.questionNum)
        for i in sameData:
            if i.id != self.id:
                i.delete()
            else:
                pass
        # try:
        #     findPQ = Question.objects.get(testID=self.testID, questionNum=(self.questionNum-1))
        #     self.prevQuestID = findPQ.questID
        #     findPQ.nextQuestID = self.questID
        #     findPQ.save()
        # except:
        #         pass
        if self.choiceFirst == "<p><br></p>":
            self.choiceFirst = None
        else:
            pass
        if self.choiceSecond == "<p><br></p>":
            self.choiceSecond= None
        else:
            pass
        if self.choiceThird  == "<p><br></p>":
            self.choiceThird = None
        else:
            pass
        if self.choiceFourth == "<p><br></p>":
            self.choiceFourth= None
        else:
            pass
        if self.choiceFifth  == "<p><br></p>":
            self.choiceFifth = None
        else:
            pass
        if self.choiceSixth  == "<p><br></p>":
            self.choiceSixth = None
        else:
            pass

        max_score = 0
        for i in Question.objects.filter(testID=self.testID):
            max_score += i.trueScore
        findPack.maxScore = max_score
        super().save(*args, **kwargs)

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
        return "{}.{}_{}".format(self.questionNum,self.testID,self.question)

class Answer(models.Model):
    def generate_id():
        digits = '0123456789'
        letters = 'abcdef'
        all_chars = digits + letters
        length = 16
        while True:
            val = ''.join(random.choice(all_chars) for i in range(length))
            if not val.isdigit():
                break
        return val

    def generate_sessionkey():
        '''Generate an 10-character Integer'''
        rand = ''.join([random.choice(string.digits) for n in range(10)])
        try:
            # if this possible ID exists, run again:
            Answer.objects.get(session_key=rand)
            return self.generate_sessionkey()
        except:
            return rand
    answerID = models.CharField(max_length=16, default=generate_id , editable=True)
    testTakerID = models.CharField(max_length=16)
    session_key = models.CharField(max_length=16)
    testID = models.CharField(max_length=16)
    questionID = models.CharField(max_length=16)
    num_ofAnswer = models.IntegerField(default=0)
    answer = models.CharField(max_length=4096,null=True, blank= True )
    scoreObtain = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.pk and self.num_ofAnswer == 1:
            findTaker = TestTaker.objects.get(testTakerID=self.testTakerID, session_key=self.session_key)
            findTaker.startTime = datetime.datetime.now()
            findTaker.save()
            super(Answer, self).save(*args, **kwargs)
        try:
            findQuest = Answer.objects.get(questionID=self.questionID, testTakerID=self.testTakerID)
        except:
            pass
        try:
            # for update score in TestTaker
            #Querysets:
            findAnswer = Answer.objects.filter(testTakerID=self.testTakerID, session_key=self.session_key)
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

            findTaker = Answer.objects.filter(testTakerID==self.testTakerID, session_key=self.session_key)
            findTestTaker = TestTaker.objects.get(testTakerID=self.testTakerID)
            if self.num_ofAnswer == 1:
                findTestTaker.firstAnswerID = self.answerID
                findTestTaker.save()
            else:
                pass

            findPA = Answer.objects.get(questionID=self.questionID, testTakerID=self.testTakerID, num_ofAnswer=(self.num_ofAnswer-1))
            self.prevAnswerID = findPA.answerID
            findPA.nextQuestID = self.answerID
            findPA.save()
        except:
            pass

        sameData = Answer.objects.filter(session_key=self.session_key, testID=self.testID, questionID=self.questionID)
        for i in sameData:
            if i.id != self.id:
                i.delete()
            else:
                pass
        super(Answer, self).save(*args, **kwargs)

    def __str__(self):
        return "{} for {}".format(self.testTakerID , self.questionID)

class TestTaker(models.Model):
    def generate_id(*args, **kwargs,):
        '''Generate an 8-character long hexadecimal ID'''
        possible = str(hexlify(os.urandom(8)))
        possible = possible[2:18]
        try:
            # if this possible ID exists, run again:
            TestTaker.objects.get(testTakerID=possible)
            return self.generate_id()
        except :
            return possible

    testTakerID = models.CharField(max_length=16, default=generate_id(), editable=True,)
    session_key = models.CharField(max_length=16, editable=True)
    session_password = models.CharField(max_length=16)
    testID = models.CharField(max_length=16)
    testTakerName = models.CharField(max_length=128)
    testTakerGroup = models.CharField(max_length=128 ,blank=True ,null=True)
    scoreObtained = models.IntegerField(default=0)
    lastAnswered = models.IntegerField(default=0, editable=True)
    timeStart = models.DateTimeField(auto_now_add=False,editable=True, null=True,blank=True,default=datetime.datetime.now())
    timeFinish = models.DateTimeField(auto_now_add=False,editable=True, null=True,blank=True,default=datetime.datetime.now())

    def save(self,*args, **kwargs):
        try :
            User.objects.get(username=self.session_key)
        except:
            user = User.objects.create_user(self.session_key, None, self.session_password)
            user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}({})".format(self.testTakerID,self.testTakerName)

class TestWelcome(models.Model):
    testID = models.CharField(max_length=16)
    welcomeMessage = models.TextField()
    def save(self,*args, **kwargs):
        findPack = TestPackage.objects.get(testID=self.testID)
        findPack.welcomeMessageID = self.id
        super().save()
