from django.urls import path
from .views import *

urlpatterns = [
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('about/', AboutView.as_view(), name='about'),

    path('', WordList.as_view(), name='words'),
    path('word/<int:pk>/', WordDetail.as_view(), name='word'),
    path('word-create/', WordCreate.as_view(), name='word-create'),
    path('word-update/<int:pk>', WordUpdate.as_view(), name='word-update'),
    path('word-delete/<int:pk>', WordDelete.as_view(), name='word-delete'),

    path('api/', apiOverview, name='api-overview'),
    path('api/word/', wordList, name='api-word-list'),
    path('api/word/<int:pk>/', wordDetail, name='api-word-detail'),
    path('api/word-create/', wordCreate, name='api-word-create'),
    path('api/word-update/<int:pk>', wordUpdate, name='api-word-update'),
    path('api/word-delete/<int:pk>', wordDelete, name='api-word-delete'),
]
