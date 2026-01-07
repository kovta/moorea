"""Database configuration and models."""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database URL - Supports Supabase and other PostgreSQL providers
# Priority: DATABASE_URL env var > settings.database_url > localhost fallback
DATABASE_URL = (
    os.getenv("DATABASE_URL") 
    or os.getenv("SUPABASE_DATABASE_URL")  # Supabase-specific env var
    or "postgresql://kovacstamaspal@localhost/moorea"  # Local fallback
)

# Log database URL (mask password for security)
if DATABASE_URL:
    # Mask password in URL for logging
    import re
    masked_url = re.sub(r':([^:@]+)@', r':****@', DATABASE_URL)
    print(f"🔗 Database URL: {masked_url}")
    
    # Warn if using localhost fallback (means DATABASE_URL not set)
    if "localhost" in DATABASE_URL:
        print("⚠️  WARNING: Using localhost fallback - DATABASE_URL not set in environment!")
        print("⚠️  Set DATABASE_URL in Railway → Variables tab")
else:
    print("❌ ERROR: No DATABASE_URL found!")

# Create engine with connection pooling and retry logic
# This prevents connection exhaustion and handles temporary connection failures
engine = create_engine(
    DATABASE_URL,
    pool_size=5,  # Number of connections to keep in pool
    max_overflow=10,  # Additional connections that can be created on demand
    pool_pre_ping=True,  # Verify connections before using (handles dropped connections)
    pool_recycle=3600,  # Recycle connections after 1 hour (prevents stale connections)
    connect_args={
        "connect_timeout": 10,  # 10 second connection timeout
        "options": "-c statement_timeout=30000"  # 30 second query timeout
    }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    """User model for authentication."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to moodboards
    moodboards = relationship("Moodboard", back_populates="owner")

class Moodboard(Base):
    """Moodboard model for saving user moodboards."""
    __tablename__ = "moodboards"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    aesthetic = Column(String, nullable=False)  # The detected aesthetic
    images = Column(JSON, nullable=False)  # List of image URLs and metadata
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to user
    owner = relationship("User", back_populates="moodboards")

class WaitlistUser(Base):
    """Waitlist signup model for pre-launch email collection."""
    __tablename__ = "waitlist_users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)  # Optional
    created_at = Column(DateTime, default=datetime.utcnow)
    notified = Column(Boolean, default=False)  # Track if we've sent launch email

def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
