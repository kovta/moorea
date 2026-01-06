# Supabase Setup Guide

## Step 1: Create Supabase Account

1. Go to https://supabase.com
2. Click "Start your project" or "Sign up"
3. Sign up with GitHub (easiest) or email

## Step 2: Create a New Project

1. Click "New Project"
2. **Organization**: Create new or select existing
3. **Project Details**:
   - **Name**: `moorea-backend` (or any name you prefer)
   - **Database Password**: Generate a strong password (SAVE THIS!)
   - **Region**: Choose closest to you (e.g., `US East`)
4. Click "Create new project"
5. Wait 2-3 minutes for setup to complete

## Step 3: Get Your Database Connection String

1. Go to your project dashboard
2. Click **Settings** (gear icon) in the left sidebar
3. Click **Database** in the settings menu
4. Scroll down to **Connection string**
5. Under **Connection pooling**, select **Transaction** mode
6. Copy the connection string (looks like this):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```

## Step 4: Update Environment Variables

1. In your backend `.env` file, add:
   ```bash
   DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```
   Replace `[YOUR-PASSWORD]` with your actual password

2. Or set it in Railway/Vercel environment variables when deploying

## Step 5: Create Database Tables

Your tables will be automatically created when the app starts (via `create_tables()`), but you can also run:

```python
python -c "from database import create_tables; create_tables()"
```

Or they'll auto-create on first backend startup.

## Step 6: Verify Connection

1. Start your backend: `python -m uvicorn app.main:app --reload`
2. Check logs - should see "Database tables created"
3. Test waitlist signup: `curl -X POST http://localhost:8000/api/v1/waitlist/subscribe -H "Content-Type: application/json" -d '{"email":"test@example.com"}'`

## Supabase Dashboard Features

Once set up, you can:
- View your data in **Table Editor**
- Run SQL queries in **SQL Editor**
- Monitor usage in **Project Settings**

## Important Notes

- **Free tier includes**: 500 MB database, unlimited API requests
- **Database password**: Keep this secure! Never commit it to git.
- **Connection pooling**: Use "Transaction" mode for FastAPI/SQLAlchemy
- **Backups**: Free tier includes daily backups

## Troubleshooting

**Connection refused?**
- Check your database password is correct
- Make sure you're using the right connection string (Transaction mode)
- Check Supabase project is active (not paused)

**Tables not creating?**
- Check DATABASE_URL is set correctly
- Look for errors in backend logs
- Verify SQLAlchemy can connect

**Need to reset?**
- Supabase dashboard → Settings → Database → Reset Database (careful!)




