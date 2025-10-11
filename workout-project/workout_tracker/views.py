from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .models import Workout, Exercise, PersonalRecord, Badge, UserBadge
from .serializer import WorkoutSerializer, ExerciseSerializer, PersonalRecordSerializer, BadgeSerializer, UserBadgeSerializer, UserSerializer

User = get_user_model()

class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all().order_by('-date')
    serializer_class = WorkoutSerializer
    # permission_classes = [IsAuthenticated,]

    # def get_queryset(self):
    #     return self.queryset.filter(user=self.request.user).order_by('-date')
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    # permission_class = [IsAuthenticated,]

class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    # permission_classes = [IsAuthenticated,]

class UserBadgeViewSet(viewsets.ModelViewSet):
    queryset = UserBadge.objects.all()
    serializer_class = UserBadgeSerializer
    # permission_classes = [IsAuthenticated,]

    # def get_queryset(self):
    #     return self.queryset.filter(user=self.request.user)
    
class PersonalRecordViewSet(viewsets.ModelViewSet):
    queryset = PersonalRecord.objects.all()
    serializer_class = PersonalRecordSerializer
    # permission_classes = [IsAuthenticated,]

    # def get_queryset(self):
    #     return self.queryset.filter(user=self.request.user)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    