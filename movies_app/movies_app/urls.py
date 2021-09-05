from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from movies import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movies.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/signup/viewer/', views.ViewerSignUpView.as_view(), name='viewer_signup'),
    path('accounts/signup/manager/', views.ManagerSignUpView.as_view(), name='manager_signup'),
]
