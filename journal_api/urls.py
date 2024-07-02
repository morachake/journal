from django.urls import path
from .views import UserCreate, UserLogin, UserProfile, JournalEntryListCreate, JournalEntryDetail, CategoryListCreate, CategoryDetail, JournalSummary

urlpatterns = [
    path('register/', UserCreate.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('entries/', JournalEntryListCreate.as_view(), name='journalentry-list-create'),
    path('entries/<int:pk>/', JournalEntryDetail.as_view(), name='journalentry-detail'),
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('summary/', JournalSummary.as_view(), name='journal-summary'),
]
