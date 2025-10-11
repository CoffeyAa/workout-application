from django.urls import path, include
from rest_framework.routers import DefaultRouter

from workout_tracker import views

router = DefaultRouter()
router.register("workouts", views.WorkoutViewSet, basename="workouts")
router.register("exercises", views.ExerciseViewSet, basename="exercises")
router.register("badges", views.BadgeViewSet, basename="badges")
router.register("user-badges", views.UserBadgeViewSet, basename="user-badges")
router.register("users", views.UserViewSet, basename="user")

urlpatterns = [
    path('', include(router.urls))
]