from rest_framework import serializers
from django.shortcuts import render
from django.contrib.auth import get_user_model

from .models import Workout, Exercise, PersonalRecord, ExerciseCategory, BodyPart, Badge, ExerciseImage, UserBadge

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "email", 
            "first_name", 
            "last_name",
        ]


class ExcersieCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseCategory
        fields = [
            "name",
        ]


class BodyPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyPart
        fields = ["name", "icon"]


class ExcersieImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseImage
        fields = [
            "image",
            "display_order",
        ]


class ExerciseSerializer(serializers.ModelSerializer):
    body_parts = BodyPartSerializer(many=True, read_only=True)
    categories = ExcersieCategorySerializer(many=True, read_only=True)
    images = ExcersieImageSerializer(many=True, read_only=True)

    class Meta:
        model = Exercise
        fields = [
            "name",
            "instructions",
            "categories",
            "body_parts",
            "is_weighted",
            "is_timed",
            "images",
        ]



class WorkoutSerializer(serializers.ModelSerializer):
    exercises = serializers.StringRelatedField(many=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Workout
        fields = [
            "name",
            "user",
            "date",
            "duration_seconds",
            "exercises"
        ]


class WorkoutExcerciseSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        fields = [
            "reps",
            "weight",
            "duration_seconds",
            "order",
            "weight_unit",
        ]


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer(read_only=True)
    workout = WorkoutSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    sets = WorkoutExcerciseSetSerializer(many=True, read_only=True)

    class Meta:
        model = Exercise
        fields = [
            "workout",
            "exercise",
            "user",
            "sets",
            "distance",
            "dsitance_unit",
        ]


class PersonalRecordSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    exercise = ExerciseSerializer(read_only=True)
    workout = WorkoutSerializer(read_only=True)

    class Meta:
        model = PersonalRecord
        fields = [
            "user",
            "exercise",
            "workout",
            "best_weight",
            "weight_unit",
            "best_reps",
            "best_duration_seconds",
            "best_distance",
            "distance_unit",
            "achieved_date",
        ]


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = [
            "name",
            "description",
            "icon",
            "start_date",
            "end_date",
            "category",
        ]


class UserBadgeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    badge = BadgeSerializer(read_only=True)

    class Meta:
        model = UserBadge
        fields = [
            "user",
            "badge",
            "achieved_date",
        ]
