from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .models import JournalEntry, Category
from .serializers import UserSerializer, JournalEntrySerializer, CategorySerializer, UserProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserLogin(TokenObtainPairView):
    pass

class UserProfile(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

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

class CategoryListCreate(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Short-circuit for swagger_fake_view
        if getattr(self, 'swagger_fake_view', False):
            return Category.objects.none()
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class JournalSummary(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        entries = JournalEntry.objects.filter(user=user)
        summary = entries.values('category__name').annotate(count=Count('id'))
        return Response(summary)