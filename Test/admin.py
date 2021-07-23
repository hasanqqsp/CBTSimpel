from django.contrib import admin
from .models import (TestPackage , Question, Answer, TestTaker)

admin.site.register(Answer)
admin.site.register(TestTaker)
admin.site.register(Question)
admin.site.register(TestPackage)