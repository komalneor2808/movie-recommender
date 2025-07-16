# This file handles user login, signup, and password 
# I am using SQLite database to store user information

import sqlite3
import bcrypt  # for password security
import streamlit as st
from datetime import datetime
import os

class UserAuth:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.setup_database()
    
    def setup_database(self):

        # Create the database table if it doesn't exist already
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # This creates the users table with all the required columns 
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                age INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                theme_preference TEXT DEFAULT 'light'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def make_password_secure(self, password):
        # Hash the password so we don't store plain text passwords
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    def check_password(self, password, stored_hash):
        # Check if the entered password matches the stored hash
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
    
    def create_user(self, username, email, password, full_name="", age=None):
        # Add a new user to the database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Make password secure before storing
            secure_password = self.make_password_secure(password)
            
            # Insert new user into database
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name, age)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, secure_password, full_name, age))
            
            conn.commit()
            conn.close()
            return True, "Account created successfully!"
        
        except sqlite3.IntegrityError as e:
            conn.close()
            # Check what went wrong
            if "username" in str(e):
                return False, "This username is already taken!"
            elif "email" in str(e):
                return False, "This email is already registered!"
            else:
                return False, "Something went wrong while creating the account!"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    def authenticate_user(self, username, password):
        # Check if username and password are correct
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get the stored password hash for this username
        cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        
        # If user exists and password matches, return True
        if result and self.check_password(password, result[0]):
            return True
        return False
    
    def get_user_info(self, username):
        # Get all info about a user
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT username, email, full_name, age, created_at, theme_preference 
            FROM users WHERE username = ?
        ''', (username,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            # Return user info as a dictionary
            return {
                'username': result[0],
                'email': result[1],
                'full_name': result[2],
                'age': result[3],
                'created_at': result[4],
                'theme_preference': result[5]
            }
        return None
    
    def update_user_info(self, username, email=None, full_name=None, age=None):
        # Update user profile information
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Build the update query acc. to provided fields
            updates = []
            params = []
            
            if email:
                updates.append("email = ?")
                params.append(email)
            if full_name is not None:
                updates.append("full_name = ?")
                params.append(full_name)
            if age is not None:
                updates.append("age = ?")
                params.append(age)
            
            # Only update if there is something to update
            if updates:
                params.append(username)
                query = f"UPDATE users SET {', '.join(updates)} WHERE username = ?"
                cursor.execute(query, params)
                conn.commit()
            
            conn.close()
            return True, "Profile updated!"
        
        except sqlite3.IntegrityError:
            conn.close()
            return False, "That email is already being used!"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    def change_password(self, username, old_password, new_password):
        # Change user's password after checking if the old password is correct
        if not self.authenticate_user(username, old_password):
            return False, "Your current password is wrong!"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Hash the new password and update it
            new_hash = self.make_password_secure(new_password)
            cursor.execute('UPDATE users SET password_hash = ? WHERE username = ?', 
                         (new_hash, username))
            conn.commit()
            conn.close()
            return True, "Password changed!"
        
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    def update_theme_preference(self, username, theme):
        # Save user's theme preference between light/dark
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('UPDATE users SET theme_preference = ? WHERE username = ?', 
                         (theme, username))
            conn.commit()
            conn.close()
            return True
        except Exception:
            conn.close()
            return False

# Create the auth object that will be used in other files
auth = UserAuth()
