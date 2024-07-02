from django.contrib.auth.models import User
from rest_framework import serializers
from .models import JournalEntry, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
       user = User.objects.create_user(
           username=validated_data['username'],
           email=validated_data['email'],
           password=validated_data['password']
       )
       return user
   
class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ('id', 'user', 'title', 'content', 'category', 'date')
