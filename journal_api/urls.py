from django.urls import path
from .views import UserCreate, UserLogin, JournalEntryListCreate, JournalEntryDetail

urlpatterns = [
    path('register/', UserCreate.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('entries/', JournalEntryListCreate.as_view(), name='journalentry-list-create'),
    path('entries/<int:pk>/', JournalEntryDetail.as_view(), name='journalentry-detail'),
]
