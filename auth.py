import sqlite3
import bcrypt
import streamlit as st
from datetime import datetime
import os

class UserAuth:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
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
    
    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    def verify_password(self, password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    
    def create_user(self, username, email, password, full_name="", age=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            password_hash = self.hash_password(password)
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name, age)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, password_hash, full_name, age))
            
            conn.commit()
            conn.close()
            return True, "User created successfully!"
        
        except sqlite3.IntegrityError as e:
            conn.close()
            if "username" in str(e):
                return False, "Username already exists!"
            elif "email" in str(e):
                return False, "Email already exists!"
            else:
                return False, "User creation failed!"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    def authenticate_user(self, username, password):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result and self.verify_password(password, result[0]):
            return True
        return False
    
    def get_user_info(self, username):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT username, email, full_name, age, created_at, theme_preference 
            FROM users WHERE username = ?
        ''', (username,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
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
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
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
            
            if updates:
                params.append(username)
                query = f"UPDATE users SET {', '.join(updates)} WHERE username = ?"
                cursor.execute(query, params)
                conn.commit()
            
            conn.close()
            return True, "Profile updated successfully!"
        
        except sqlite3.IntegrityError:
            conn.close()
            return False, "Email already exists!"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    def change_password(self, username, old_password, new_password):
        if not self.authenticate_user(username, old_password):
            return False, "Current password is incorrect!"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            new_hash = self.hash_password(new_password)
            cursor.execute('UPDATE users SET password_hash = ? WHERE username = ?', 
                         (new_hash, username))
            conn.commit()
            conn.close()
            return True, "Password changed successfully!"
        
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    def update_theme_preference(self, username, theme):
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

auth = UserAuth()
