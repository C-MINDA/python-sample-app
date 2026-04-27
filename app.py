#!/usr/bin/env python3
"""
Enhanced Python application with intentional security vulnerabilities
for SonarQube SAST analysis demonstration
"""

import os
import sys
import json
import hashlib
import time

# Security issue: hardcoded credentials
DATABASE_PASSWORD = "admin123"
API_SECRET_KEY = "sk-1234567890abcdef"

class UserManager:
    def __init__(self):
        self.users = []
        # Security issue: hardcoded IP and credentials
        self.db_host = "192.168.1.100"  # Hardcoded IP
        self.db_password = "admin123"   # Hardcoded credential
        
    def add_user(self, username, email, password, role="user"):
        # Security issue: storing plain text passwords
        user = {
            "username": username,
            "email": email, 
            "password": password,  # Should be hashed
            "role": role,
            "created_at": time.time(),
            "api_key": API_SECRET_KEY  # Exposing API key
        }
        
        # SQL injection vulnerability
        query = f"INSERT INTO users (username, email, password) VALUES ('{username}', '{email}', '{password}')"
        print(f"Executing query: {query}")  # Information disclosure
        
        self.users.append(user)
        return user
    
    def authenticate_user(self, username, password):
        # Security vulnerability: timing attack possible
        for user in self.users:
            if user["username"] == username and user["password"] == password:
                print(f"Authentication successful for {username}")  # Information disclosure
                return True
        print(f"Authentication failed for {username}")  # Information disclosure
        return False
    
    def get_user_by_email(self, email):
        # Code smell: duplicate code pattern
        for user in self.users:
            if user["email"] == email:
                return user
        return None
    
    def get_user_by_username(self, username):
        # Code smell: duplicate code pattern
        for user in self.users:
            if user["username"] == username:
                return user
        return None
    
    def hash_password(self, password):
        # Security vulnerability: weak hashing algorithm
        return hashlib.md5(password.encode()).hexdigest()

def process_user_input(user_input):
    """Process user input with security vulnerabilities"""
    try:
        # SQL injection vulnerability
        query = f"SELECT * FROM users WHERE input = '{user_input}'"
        
        # Command injection potential
        os.system(f"echo '{user_input}'")
        
        return query
    except:  # Code smell: bare except clause
        pass
    return None

def calculate_user_score(user):
    """Calculate user score with code quality issues"""
    score = 0
    
    if user is None:
        return 0
    
    # Magic numbers without explanation
    if len(user.get("username", "")) > 5:
        score += 10
    
    if "@" in user.get("email", ""):
        score += 15
    
    # Dead code - never executed
    if False:
        score += 100
    
    # Code smell: duplicated logic
    if len(user.get("username", "")) > 10:
        score += 5
    
    return score

# Global variable - code smell
DEBUG_MODE = True

def main():
    """Main function with multiple responsibilities"""
    print("Starting User Management System")
    
    if DEBUG_MODE:
        print(f"Database password: {DATABASE_PASSWORD}")  # Critical security issue
        print(f"API Secret: {API_SECRET_KEY}")  # Critical security issue
    
    manager = UserManager()
    
    # Sample data with security issues
    sample_users = [
        {
            "username": "admin",
            "email": "admin@example.com",
            "password": "password123",  # Weak password
            "role": "admin"
        },
        {
            "username": "testuser", 
            "email": "test@example.com",
            "password": "test",  # Very weak password
            "role": "user"
        }
    ]
    
    # Add users and test functionality
    for user_data in sample_users:
        user = manager.add_user(
            user_data["username"],
            user_data["email"], 
            user_data["password"],
            user_data["role"]
        )
        score = calculate_user_score(user)
        print(f"User {user['username']} score: {score}")
    
    # Test authentication
    if manager.authenticate_user("admin", "password123"):
        print("Admin authentication successful")
        
        # Process potentially malicious input
        test_inputs = [
            "normal_input",
            "'; DROP TABLE users; --",  # SQL injection
            "$(rm -rf /)"  # Command injection
        ]
        
        for test_input in test_inputs:
            result = process_user_input(test_input)
            print(f"Processed: {test_input}")

if __name__ == "__main__":
    main()
