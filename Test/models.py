from django.db import models
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login
import datetime
from utils.generate_id import generate_id
import json

class TestPackage(models.Model):
    testID = models.CharField(max_length=16, unique=True,editable=False,blank=True)
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
    
    def get_one_question(self,num,*args):
        print(args[0])
        if len(args) > 0:
            num = args[0][num-1]
        else:
            num -= 1
        return self.question_set.all()[num]
'''
from Test.models import *
all = TestPackage.objects.all()
a1=all[1]
a1.get_one_question(1,a1.get_random_sequence())
'''
    def get_max_score(self):
        list = []
        for i in self.question_set.all():
            list.append(i.trueScore)
        return sum(list)
        
class TestTaker(models.Model):
    testTakerID = models.CharField(max_length=16, unique=True,editable=True)
    session_code = models.CharField(max_length=16, unique=True, editable=True)
    session_password = models.CharField(max_length=16)
    testPackage = models.ForeignKey(TestPackage,on_delete=models.CASCADE)
    testTakerName = models.CharField(max_length=128)
    testTakerGroup = models.CharField(max_length=128 ,blank=True ,null=True)
    timeStart = models.DateTimeField(auto_now_add=False,editable=True, null=True,blank=True,default=datetime.datetime.now())
    timeFinish = models.DateTimeField(auto_now_add=False,editable=True, null=True,blank=True,default=datetime.datetime.now())
    sequences = models.JSONField(blank=True,null=True)
    def save(self,*args, **kwargs):
        if not self.sequences:
            self.sequences = json.dumps(self.testPackage.get_random_sequence())
            
        if not User.objects.filter(username=self.session_code).exists()
            user = User.objects.create_user(self.session_code, None, self.session_password)
            user.save()
        super().save(*args, **kwargs)
    
    def get_all_answers(self):
        return self.answer_set.all()
        
    def get_score(self):
        list = []
        for i in self.answer_set.all():
            if i.isTrue:
                list.append(i.trueScore)
                
            elif i.isTrue = False:
                list.append(i.falseScore)
            else:
                list.append(i.defaultScore)
        return sum(list)
    
    def get_last_answered(self):
        return self.answer_set.all().order_by('-timeStamp')[0]
    
    def timeStart(self):
        self.timeStart = datetime.datetime.now()
        super().save()
        
    def timeEnd(self):
        self.timeFinish = datetime.datetime.now()
        super().save()
    
    def __str__(self):
        return "{}({})".format(self.testTaker,self.testTakerName)

class Question(models.Model):

    questID = models.CharField(max_length=16, unique = True, editable=True)
    questionNum = models.IntegerField(default=0)
    question = models.TextField()
    testPackage = models.ForeignKey(TestPackage,on_delete=models.CASCADE)
    choices = models.JSONField(blank=True,null=True)
    answerKey = models.CharField(max_length=1024,default=None, blank=True, null=True)
    trueScore = models.FloatField(default=0)
    defaultScore = models.FloatField(default=0)
    falseScore = models.FloatField(default=0)
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
        try:
            findPQ = Question.objects.get(testID=self.testID, questionNum=(self.questionNum-1))
            self.prevQuestID = findPQ.questID
            findPQ.nextQuestID = self.questID
            findPQ.save()
        except:
                pass
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

    def __str__(self):
         return "{}_{}".format(self.TestPackage,self.questTitle)

class Answer(models.Model):
    answerID = models.CharField(max_length=16, default=generate_id , editable=True)
    testTaker = models.ForeignKey(TestTaker,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    answer = models.JSONField(blank=True,null=True)
    timeStamp = models.DateTimeField(auto_now=True)
    isTrue = models.BooleanField(default=None,null=True,blank=True)

    def __str__(self):
        return "{} for {}".format(self.testTakerID , self.questionID)

