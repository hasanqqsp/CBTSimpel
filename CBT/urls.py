from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name="homepage"),
    path('test/',include('Test.urls', namespace='test') ),
    path('createtest/', include('CreateTest.urls',namespace='create'))
]
