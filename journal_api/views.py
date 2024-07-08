from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import JournalEntry, Category
from .serializers import UserSerializer, UserProfileSerializer, JournalEntrySerializer, CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from datetime import datetime, timedelta
import pytz
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Create a new user",
        responses={201: UserSerializer()}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UserLogin(TokenObtainPairView):
    @swagger_auto_schema(
        operation_description="Login user and get JWT tokens",
        responses={200: 'JWT token response'}
    )
    def post(self, request, *args, **kwargs):
        if request.content_type != 'application/json':
            return Response({"detail": f"Unsupported media type \"{request.content_type}\" in request."}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        return super().post(request, *args, **kwargs)

class UserProfile(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve or update authenticated user profile",
        responses={200: UserProfileSerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve or update authenticated user profile",
        responses={200: UserProfileSerializer()}
    )
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def get_object(self):
        return self.request.user

class JournalEntryListCreate(generics.ListCreateAPIView):
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all journal entries for the authenticated user or create a new journal entry",
        responses={200: JournalEntrySerializer(many=True)}
    )
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return JournalEntry.objects.none()
        return JournalEntry.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        operation_description="List all journal entries for the authenticated user or create a new journal entry",
        responses={201: JournalEntrySerializer()}
    )
    def post(self, request, *args, **kwargs):
        print("Request data:", request.data)  # Add this line to print request data
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class JournalEntryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve, update, or delete a specific journal entry",
        responses={200: JournalEntrySerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve, update, or delete a specific journal entry",
        responses={200: JournalEntrySerializer()}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve, update, or delete a specific journal entry",
        responses={204: 'No Content'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return JournalEntry.objects.none()
        return JournalEntry.objects.filter(user=self.request.user)

class CategoryListCreate(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all categories for the authenticated user or create a new category",
        responses={200: CategorySerializer(many=True)}
    )
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Category.objects.none()
        return Category.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        operation_description="List all categories for the authenticated user or create a new category",
        responses={201: CategorySerializer()}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve, update, or delete a specific category",
        responses={200: CategorySerializer()}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve, update, or delete a specific category",
        responses={200: CategorySerializer()}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve, update, or delete a specific category",
        responses={204: 'No Content'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Category.objects.none()
        return Category.objects.filter(user=self.request.user)

class JournalSummary(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get a summary of journal entries over a selected period (daily, weekly, monthly)",
        manual_parameters=[
            openapi.Parameter('period', openapi.IN_QUERY, description="Period to filter journal entries", type=openapi.TYPE_STRING)
        ],
        responses={200: 'Summary of journal entries'}
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        period = request.query_params.get('period', 'daily')
        
        now = datetime.now(pytz.utc)

        if period == 'daily':
            start_date = now - timedelta(days=1)
        elif period == 'weekly':
            start_date = now - timedelta(weeks=1)
        elif period == 'monthly':
            start_date = now - timedelta(days=30)
        else:
            return Response({"error": "Invalid period parameter"}, status=400)

        entries = JournalEntry.objects.filter(user=user, date__gte=start_date)
        summary = entries.values('category__name').annotate(count=Count('id'))
        
        return Response(summary)
