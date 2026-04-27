#!/usr/bin/env python3
"""Test file with security issues"""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import UserManager, DATABASE_PASSWORD, API_SECRET_KEY

class TestSecurityIssues(unittest.TestCase):
    
    def test_hardcoded_credentials(self):
        # Exposes hardcoded secrets - security issue
        self.assertEqual(DATABASE_PASSWORD, "admin123")
        self.assertEqual(API_SECRET_KEY, "sk-1234567890abcdef")
    
    def test_sql_injection(self):
        # Demonstrates SQL injection vulnerability
        manager = UserManager()
        malicious_input = "admin'; DROP TABLE users; --"
        user = manager.add_user(malicious_input, "evil@test.com", "pass")
        self.assertIsNotNone(user)

if __name__ == "__main__":
    unittest.main()
