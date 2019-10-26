from django.urls import path
from .views import (
    UserDetail,
    UserCreate,
    UserUpdate,
    UserLoginView,
    UserLogoutView,
    UserPasswordChangeView,
    UserPasswordChangeDoneView,
    UserPasswordResetView,
    UserPasswordResetDoneView,
    UserPasswordResetConfirmView,
    UserPasswordResetCompleteView
)


urlpatterns = [
    path('registration/', UserCreate.as_view(), name='user-create'),
    path('user/', UserDetail.as_view(), name='user-detail'),
    path('update/', UserUpdate.as_view(), name='user-update'),
    path('login/', UserLoginView.as_view()),
    path('logout/', UserLogoutView.as_view()),
    path('password_change/', UserPasswordChangeView.as_view(), name='password-change'),
    path('password_change/done/', UserPasswordChangeDoneView.as_view()),
    path('password_reset/', UserPasswordResetView.as_view()),
    path('password_reset/done/', UserPasswordResetDoneView.as_view()),
    path('reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view()),
    path('reset/done/', UserPasswordResetCompleteView.as_view())
]
