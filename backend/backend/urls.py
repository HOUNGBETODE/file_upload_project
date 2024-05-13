# backend/urls.py

"""
URL configuration for gitapis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from users.views import signup_view, looking_for_username, query_register_username
from authentication.views import login_view, otp_view, otp_resend_view, home_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from files.views import FileAPIView, token_verification
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from files.views import upload_form_view
from django.urls import path, include
from django.shortcuts import redirect
from users.views import signup_view
from django.contrib import admin
from django.conf import settings

# this view redirects the user to the login page when he/she does not provide any endpoint
def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('login')


urlpatterns = [
    path('admin/', admin.site.urls),

    # paths for authentication app
    path('login/', login_view, name='login'), # to login user
    path('logout/', LogoutView.as_view(), name='logout'),
    path('give-otp-code/', otp_view, name="otp-v"),
    path('otp-resent/', otp_resend_view, name='otp-r'),
    path('captcha/', include('captcha.urls')),
    path('home/', home_view, name='home'),
    path('', index),

    # path for files app
    path('file/', upload_form_view, name='up-file'),
    path('api/file/', FileAPIView.as_view()),
    path('api/file/<int:file_id>', FileAPIView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify', token_verification),

    # paths for users app
    path('register/', signup_view, name='register'), # to register users
    path('username/', looking_for_username),
    path('uregister/', query_register_username),
]


# this is to serve static files via media url in browser
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
