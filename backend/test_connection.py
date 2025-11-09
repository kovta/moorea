#!/usr/bin/env python3
"""Test Supabase connection with different password encodings."""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus, urlparse, urlunparse

load_dotenv()

db_url = os.getenv('DATABASE_URL', '')
if not db_url:
    print("❌ DATABASE_URL not found in .env")
    exit(1)

print("Testing connection with different password encodings...\n")

# Parse the connection string manually
try:
    # Split the URL
    if not db_url.startswith('postgresql://'):
        print("❌ Invalid connection string format")
        exit(1)
    
    # Extract parts manually
    remaining = db_url.replace('postgresql://', '')
    if '@' not in remaining:
        print("❌ No @ found in connection string")
        exit(1)
    
    user_pass, rest = remaining.split('@', 1)
    if ':' not in user_pass:
        print("❌ No password found in connection string")
        exit(1)
    
    username, password = user_pass.split(':', 1)
    
    print(f"Username: {username}")
    print(f"Password length: {len(password)}")
    print(f"Password ends with: ...{password[-5:]}")
    print()
    
    # Test 1: Original connection string
    print("Test 1: Original connection string")
    try:
        engine = create_engine(db_url, pool_pre_ping=True)
        with engine.connect() as conn:
            result = conn.execute(text('SELECT version()'))
            print("✅ SUCCESS with original!")
            exit(0)
    except Exception as e:
        print(f"❌ Failed: {str(e)[:100]}")
    
    print()
    
    # Test 2: URL-encoded password
    print("Test 2: URL-encoded password")
    encoded_password = quote_plus(password)
    new_url = f'postgresql://{username}:{encoded_password}@{rest}'
    print(f"Trying with URL-encoded password...")
    try:
        engine = create_engine(new_url, pool_pre_ping=True)
        with engine.connect() as conn:
            result = conn.execute(text('SELECT version()'))
            print("✅ SUCCESS with URL-encoded password!")
            print(f"\n💡 Update your .env file with:")
            print(f"DATABASE_URL={new_url}")
            exit(0)
    except Exception as e:
        print(f"❌ Failed: {str(e)[:100]}")
    
    print("\n❌ Both methods failed. Please verify:")
    print("   1. Password is correct in Supabase dashboard")
    print("   2. Database password hasn't been reset")
    print("   3. Copy the connection string directly from Supabase (it should already have encoded password)")
    
except Exception as e:
    print(f"❌ Error parsing connection string: {e}")
    exit(1)

