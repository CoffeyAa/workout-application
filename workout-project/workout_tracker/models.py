from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from  django.utils import timezone

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid email address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default='', unique=True)
    first_name = models.CharField(max_length=30, blank=True, default='')
    last_name = models.CharField(max_length=30, blank=True, default='')

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.email
    
class ExerciseCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name
    
    
class BodyPart(models.Model):
    name = models.CharField(max_length=200, unique=True)
    icon = models.ImageField(upload_to="body_part_images/")

    def __str__(self) -> str:
        return self.name
    
class Exercise(models.Model):
    name = models.CharField(max_length=200, unique=True)
    instructions = models.TextField()
    categories = models.ManyToManyField(ExerciseCategory, related_name="exercises")
    body_parts = models.ManyToManyField(BodyPart, related_name="exercises")
    is_weighted = models.BooleanField(default=False)
    is_timed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class ExerciseImage(models.Model):
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="exercise_images/")
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self) -> str:
        return f"{self.exercise.name} - IMAGE {self.display_order}"


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workouts")
    date = models.DateTimeField(auto_now_add=True)
    legth = models.PositiveIntegerField(null=True, blank=True)
    exercises = models.ManyToManyField(
        Exercise,
        through="WorkoutExercise",
        related_name="workouts"
    )
    
    def __str__(self) -> str:
        return f"f{self.user.email} - {self.date.date()}"

class WorkoutExercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workout_exercises")
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="workout_exercises")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="workout_exercises")
    
    DISTANCE_CHOICES = [
        ("mi", "Miles"),
        ("km", "Kilometers")
    ]
    distance = models.FloatField(null=True, blank=True)
    distance_unit = models.CharField(
        choices=DISTANCE_CHOICES,
        null=True,
        blank=True
    )

class WorkoutSet(models.Model):
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE, related_name="sets")
    reps = models.PositiveIntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    duration_seconds = models.IntegerField(null=True, blank=True)
    order = models.IntegerField(default=1)

    UNIT_CHOICES = [
        ("kg", "Kilograms"),
        ("lb", "Pounds"),
    ]
    weight_unit = models.CharField(
        choices=UNIT_CHOICES,
        null=True,
        blank=True,
    )

    
    class Meta:
        ordering = ["order"]

    def __str__(self) -> str:
        return f"{self.workout_exercise.exercise.name} - Set {self.order}"

class PersonalRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="personal_records")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="personal_records")
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="personal_records")
    best_weight = models.FloatField(null=True, blank=True)
    weight_unit = models.CharField(
        max_length=2,
        choices=[('kg', 'Kilograms'), ('lb', 'Pounds')],
        null=True,
        blank=True
    )
    best_reps = models.IntegerField(null=True, blank=True)
    best_duration_seconds = models.IntegerField(null=True, blank=True)
    best_distance = models.FloatField(null=True, blank=True)
    distance_unit = models.CharField(
        choices=[('mi', 'Miles'), ('km', 'Kilometers')],
        null=True,
        blank=True
    )
    achieved_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PR: {self.user.email} - {self.exercise.name}"

class Badge(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    icon = models.ImageField(upload_to="badges/")
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)

    CATEGORIES = [
        ("pr", "Personal Records"),
        ("streak", "Streaks"),
        ("distance", "Distance"),
        ("monthly", "Monthly"),
        ("challenges", "Challenges"),
    ]
    category = models.CharField(
        choices=CATEGORIES,
        null=True,
        blank=True,
    )
    criteria = models.JSONField(null=True, blank=True, help_text="JSON rules")

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="badges")
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name="earned_by")
    achieved_date = models.DateTimeField(auto_now_add=True)