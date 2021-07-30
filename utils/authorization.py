from django.http import (HttpResponseRedirect)
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
adminLoginURL = reverse_lazy('create:login')
class GroupRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user:
            return HttpResponseRedirect(adminLoginURL)
        else:
            if not request.user.groups.filter(name='author').exists():
                return HttpResponseRedirect(adminLoginURL)
        return super(GroupRequiredMixin, self).dispatch(request, *args, **kwargs)

def isAdmin(request):
    if not request.user.groups.filter(name='testAuthor').exists():
        return False
    return True
# decorator
def admin_required(*args):
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name="testAuthor")):
                return True
        return False

    return user_passes_test(in_groups, login_url=adminLoginURL)