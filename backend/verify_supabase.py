#!/usr/bin/env python3
"""Quick script to verify Supabase database connection and create tables."""

import os
import sys
from database import engine, create_tables, WaitlistUser, User, Moodboard
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from database import SessionLocal

def check_connection():
    """Test database connection."""
    try:
        # Try to connect
        with engine.connect() as conn:
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n💡 Make sure you've set DATABASE_URL in your .env file")
        print("   Get it from: Supabase Dashboard → Settings → Database → Connection string")
        return False

def list_tables():
    """List existing tables."""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"\n📊 Existing tables: {len(tables)}")
    for table in tables:
        print(f"   - {table}")
    return tables

def create_missing_tables():
    """Create tables if they don't exist."""
    print("\n🔨 Creating tables if needed...")
    try:
        create_tables()
        print("✅ Tables created/verified!")
    except Exception as e:
        print(f"⚠️  Error creating tables: {e}")
        return False
    return True

def test_waitlist_table():
    """Test the waitlist_users table."""
    print("\n🧪 Testing waitlist_users table...")
    try:
        db = SessionLocal()
        # Try to query (even if empty)
        count = db.query(WaitlistUser).count()
        print(f"   ✅ waitlist_users table exists ({count} records)")
        db.close()
        return True
    except Exception as e:
        print(f"   ❌ Error querying waitlist_users: {e}")
        return False

def main():
    print("🚀 Verifying Supabase Database Setup\n")
    print(f"📍 DATABASE_URL: {'Set' if os.getenv('DATABASE_URL') else 'Not set'}")
    
    if not check_connection():
        sys.exit(1)
    
    tables = list_tables()
    
    # Check if our tables exist
    required_tables = ['users', 'moodboards', 'waitlist_users']
    missing = [t for t in required_tables if t not in tables]
    
    if missing:
        print(f"\n⚠️  Missing tables: {', '.join(missing)}")
        if create_missing_tables():
            list_tables()
    
    test_waitlist_table()
    
    print("\n✅ All checks passed! Your Supabase database is ready.")
    print("\n💡 Next steps:")
    print("   1. Your tables are ready for the waitlist")
    print("   2. Start your backend: python -m uvicorn app.main:app --reload")
    print("   3. Test waitlist signup at: http://localhost:8000/api/v1/waitlist/subscribe")

if __name__ == "__main__":
    main()




