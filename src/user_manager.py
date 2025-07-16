import json
import os
from pathlib import Path

class UserManager:
    def __init__(self):
        self.users_db_path = Path("data/users_db.json")
        self.load_users()

    def load_users(self):
        if self.users_db_path.exists():
            with open(self.users_db_path, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}

    def save_users(self):
        with open(self.users_db_path, 'w') as f:
            json.dump(self.users, f, indent=4)

    def verify_login(self, username, password):
        if username in self.users:
            return self.users[username]['password'] == password
        return False

    def register_user(self, username, password, name):
        if username in self.users:
            return False
        
        self.users[username] = {
            'password': password,
            'name': name,
            'preferences': {
                'default_min_rating': 4,
                'default_top_n': 5,
                'favorite_genres': [],
                'ui_preferences': {
                    'theme': 'light',
                    'text_size': 'medium',
                    'profile_color': '#1f77b4',
                    'accent_color': '#ff4b4b',
                    'font_family': 'sans-serif',
                    'compact_mode': False,
                    'show_animations': True,
                    'language': 'English'
                }
            },
            'settings': {
                'dark_mode': False,
                'email_notifications': False
            }
        }
        self.save_users()
        return True

    def update_preferences(self, username, preferences):
        if username in self.users:
            # Update movie preferences
            self.users[username]['preferences'].update({
                k: v for k, v in preferences.items() 
                if k in ['default_min_rating', 'default_top_n', 'favorite_genres']
            })
            # Update UI preferences if present
            if 'ui_preferences' in preferences:
                self.users[username]['preferences']['ui_preferences'].update(preferences['ui_preferences'])
            self.save_users()
            return True
        return False

    def update_settings(self, username, settings):
        if username in self.users:
            self.users[username]['settings'].update(settings)
            self.save_users()
            return True
        return False

    def get_user_data(self, username):
        return self.users.get(username, None)

    def update_user_data(self, username, user_data):
        if username in self.users:
            self.users[username] = user_data
            self.save_users()
            return True
        return False
