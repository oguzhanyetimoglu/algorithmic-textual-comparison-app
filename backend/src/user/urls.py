from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile', views.UserDetail.as_view()),
    path('manage-user', views.CreateListUser.as_view(), name='create_user'),
    path('manage-user/<int:pk>',
         views.UpdateDeleteUser.as_view(),
         name='create_user'),
]
