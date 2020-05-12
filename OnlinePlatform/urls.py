"""OnlinePlatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Auth.urls import router as auth_router
from Auth.views import verify
from Lesson.urls import router as lesson_router
router = DefaultRouter()
router.registry.extend(auth_router.registry)
router.registry.extend(lesson_router.registry)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    url(r'^verify/(?P<uuid>[a-z0-9\-]+)/', verify, name='verify'),
    url(r'mdeditor/', include('mdeditor.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

