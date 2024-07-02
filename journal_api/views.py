from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .models import JournalEntry
from .serializers import UserSerializer, JournalEntrySerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserLogin(TokenObtainPairView):
    pass

class JournalEntryListCreate(generics.ListCreateAPIView):
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Get a list of journal entries", responses={200: JournalEntrySerializer(many=True)})
    def get_queryset(self):
        # Short-circuit for swagger_fake_view
        if getattr(self, 'swagger_fake_view', False):
            return JournalEntry.objects.none()
        return JournalEntry.objects.filter(user=self.request.user)

    @swagger_auto_schema(operation_description="Create a new journal entry")
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class JournalEntryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="Retrieve, update or delete a journal entry", responses={200: JournalEntrySerializer()})
    def get_queryset(self):
        # Short-circuit for swagger_fake_view
        if getattr(self, 'swagger_fake_view', False):
            return JournalEntry.objects.none()
        return JournalEntry.objects.filter(user=self.request.user)
