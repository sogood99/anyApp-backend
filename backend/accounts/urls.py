from django.urls import path, re_path
from rest_framework.authtoken import views as auth_views

from . import views

urlpatterns = [
    path('create/', views.UserCreate.as_view(), name='account-create'),
    path('login/', auth_views.obtain_auth_token, name='login'),
    path('update/', views.UserUpdate.as_view(), name='account-update'),
    path('profile/', views.GetProfileJson.as_view(), name='get-profile'),
    path('profile/update/', views.UpdateProfile.as_view(), name='update-profile'),
    path('follow/', views.FollowView.as_view(), name='follow'),
    path('follow/detail/', views.FollowDetail.as_view(), name='follow-detail'),
    path('block/', views.BlockView.as_view(), name='block'),
    path('block/detail/', views.BlockDetail.as_view(), name='block-detail'),
]
