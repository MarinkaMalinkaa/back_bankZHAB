"""
URL configuration for bank_ZHAB project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from bank import views as bank_views
from django.urls import include, path
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'user', bank_views.UserViewSet)
router.register(r'account', bank_views.AccountViewSet)
router.register(r'card', bank_views.CardViewSet)
router.register(r'contract', bank_views.ContractViewSet)
router.register(r'transaction', bank_views.TransactionViewSet)
router.register(r'status', bank_views.StatusViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('getRandomCard/', bank_views.GetRandomCard),
    path('getRandomAccount/', bank_views.GetRandomAccount),
    path('getRandomCVC/', bank_views.GetRandomCVC),
    path('getRandomPin/', bank_views.GetRandomPin),
    path('grpc/', bank_views.my_view),
    path('online/', bank_views.admin_online),
]
