from rest_framework.authtoken.views import obtain_auth_token
from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # path("login/", obtain_auth_token, name="login"), # GET TOKEN AFTER REGISTERING
    path("register/", views.registration_view, name="register"), # BOTH FOR TOKEN AND JWT
    # path("logout/", views.logout_view, name="logout"), # ONLY FOR TOKEN AUTHENTICATION
    
    
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"), # LOGIN 
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"), 
    

]
