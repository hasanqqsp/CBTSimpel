# from Test.views import resumeTest
from django.http import (HttpResponseRedirect)
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
adminLoginURL = reverse_lazy('create:login')
resumeTestURL = reverse_lazy('test:resume')
class GroupRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user:
            return HttpResponseRedirect(adminLoginURL)
        else:
            if not request.user.groups.filter(name='testAuthor').exists():
                return HttpResponseRedirect(adminLoginURL)
        return super().dispatch(request, *args, **kwargs)

def isAdmin(request):
    if not request.user.groups.filter(name='testAuthor').exists():
        return False
    return True
# decorator
def admin_required(*args,**kwargs):
    def in_groups(u,*args,**kwargs):
        if u.is_authenticated:
            if bool(u.groups.filter(name="testAuthor")):
                return True
        return False

    return user_passes_test(in_groups, login_url=adminLoginURL)

def non_admin_required(*args,**kwargs):
    def in_groups(u,*args,**kwargs):
        if u.is_authenticated:
            if bool(u.groups.filter(name="testTaker")):
                return True
        return False

    return user_passes_test(in_groups, login_url=resumeTestURL)
