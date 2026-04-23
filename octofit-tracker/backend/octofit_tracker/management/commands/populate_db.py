from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model
from djongo import models

from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']

        # Collections
        users = db['users']
        teams = db['teams']
        activities = db['activities']
        leaderboard = db['leaderboard']
        workouts = db['workouts']

        # Clear collections
        users.delete_many({})
        teams.delete_many({})
        activities.delete_many({})
        leaderboard.delete_many({})
        workouts.delete_many({})

        # Teams
        marvel = {'name': 'Marvel', 'description': 'Marvel Superheroes'}
        dc = {'name': 'DC', 'description': 'DC Superheroes'}
        marvel_id = teams.insert_one(marvel).inserted_id
        dc_id = teams.insert_one(dc).inserted_id

        # Users
        user_data = [
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team_id': marvel_id},
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team_id': marvel_id},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team_id': dc_id},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team_id': dc_id},
        ]
        user_ids = users.insert_many(user_data).inserted_ids

        # Activities
        activity_data = [
            {'user_id': user_ids[0], 'activity': 'Running', 'duration': 30},
            {'user_id': user_ids[1], 'activity': 'Cycling', 'duration': 45},
            {'user_id': user_ids[2], 'activity': 'Swimming', 'duration': 25},
            {'user_id': user_ids[3], 'activity': 'Yoga', 'duration': 40},
        ]
        activities.insert_many(activity_data)

        # Workouts
        workout_data = [
            {'name': 'Cardio Blast', 'suggested_for': 'All'},
            {'name': 'Strength Builder', 'suggested_for': 'Advanced'},
        ]
        workouts.insert_many(workout_data)

        # Leaderboard
        leaderboard_data = [
            {'user_id': user_ids[0], 'points': 100},
            {'user_id': user_ids[1], 'points': 90},
            {'user_id': user_ids[2], 'points': 110},
            {'user_id': user_ids[3], 'points': 95},
        ]
        leaderboard.insert_many(leaderboard_data)

        # Unique index on email
        users.create_index('email', unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data'))
