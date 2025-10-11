from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
from django.contrib.auth import get_user_model

from workout_tracker.models import (
    User, ExerciseCategory, BodyPart, Exercise, ExerciseImage, Workout, WorkoutExercise,
    WorkoutExcerciseSet, PersonalRecord, Badge, UserBadge
)

fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake data for all models'

    def handle(self, *args, **kwargs):
        # Users
        User = get_user_model()
        for _ in range(5):
            User.objects.create_user(
                email=fake.unique.email(),
                password='password',
                first_name=fake.first_name(),
                last_name=fake.last_name()
            ) # type: ignore
        users = list(User.objects.all())
        print(users)

        # Exercise Categories
        category_names = ["Strength", "Cardio", "Core", "Mobility"]
        categories = [ExerciseCategory.objects.create(name=c_name) for c_name in category_names]

        # Body Parts
        body_names = ["Arms", "Shoulders", "Chest", "Back", "Legs", "Core"]
        body_parts = [BodyPart.objects.create(name=b_name, icon='body_part_images/default.png') for b_name in body_names]

        # Exercises
        exercise_names = ["Bench press", "Squat", "Row", "Shoulder Press", "Curl"]
        exercises = []
        for e_name in exercise_names:
            ex = Exercise.objects.create(
                name=e_name,
                instructions=fake.text(),
                is_weighted=random.choice([True, False]),
                is_timed=random.choice([True, False])
            )
            ex.categories.set(random.sample(categories, k=1))
            ex.body_parts.set(random.sample(body_parts, k=1))
            exercises.append(ex)

            # Exercise Images
            for i in range(random.randint(1, 3)):
                ExerciseImage.objects.create(
                    exercise=ex,
                    image='exercise_images/default.png',
                    display_order=i
                )

        # Badges
        badges = []
        for _ in range(3):
            badge = Badge.objects.create(
                name=fake.unique.word(),
                description=fake.text(),
                icon='badges/default.png',
                start_date=timezone.now(),
                end_date=timezone.now() + timezone.timedelta(days=30),
                category=random.choice([c[0] for c in Badge.CATEGORIES]),
                criteria={"min": random.randint(1, 10)}
            )
            badges.append(badge)

        # Workouts, WorkoutExercise, WorkoutExcerciseSet, PersonalRecord, UserBadge
        for user in users:
            for _ in range(2):
                workout = Workout.objects.create(
                    user=user,
                    legth=random.randint(20, 120)
                )
                workout.exercises.set(random.sample(exercises, k=2))

                # WorkoutExercise
                for ex in workout.exercises.all():
                    we = WorkoutExercise.objects.create(
                        workout=workout,
                        exercise=ex,
                        distance=random.uniform(0, 10),
                        distance_unit=random.choice(['mi', 'km'])
                    )
                    # WorkoutExcerciseSet
                    for i in range(random.randint(1, 3)):
                        WorkoutExcerciseSet.objects.create(
                            workout_exercise=we,
                            reps=random.randint(1, 20),
                            weight=random.uniform(10, 100),
                            duration_seconds=random.randint(30, 300),
                            order=i+1,
                            weight_unit=random.choice(['kg', 'lb'])
                        )

                # PersonalRecord
                PersonalRecord.objects.create(
                    user=user,
                    exercise=random.choice(exercises),
                    workout=workout,
                    best_weight=random.uniform(10, 100),
                    weight_unit=random.choice(['kg', 'lb']),
                    best_reps=random.randint(1, 20),
                    best_duration_seconds=random.randint(30, 300),
                    best_distance=random.uniform(0, 10),
                    distance_unit=random.choice(['mi', 'km']),
                    achieved_date=timezone.now()
                )

                # UserBadge
                UserBadge.objects.create(
                    user=user,
                    badge=random.choice(badges),
                    achieved_date=timezone.now()
                )

        self.stdout.write(self.style.SUCCESS('Fake data for all models generated successfully!'))