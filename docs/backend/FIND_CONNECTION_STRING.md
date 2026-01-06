# 🔍 How to Find Your Supabase Connection String

## The API Key You Have
The string you showed (`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`) is your **Supabase API key** (anon key).
- ✅ Use this for **frontend** API calls
- ❌ NOT for database connections

## What You Need: Database Connection String

The connection string looks completely different - it's a PostgreSQL URL like:
```
postgresql://postgres.djeyzevh:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

---

## Step-by-Step: Find Your Connection String

### Option 1: Settings Page (Recommended)
1. Go to your Supabase project dashboard
2. Click **Settings** (⚙️ gear icon) in the left sidebar
3. Click **"Database"** (not "API"!)
4. Scroll down to **"Connection string"** section
5. Look for **"Connection pooling"** dropdown
6. Select **"Transaction"** mode
7. Copy the connection string that starts with `postgresql://`

### Option 2: Project Settings
1. Go to your project dashboard
2. Click **"Project Settings"** (gear icon at bottom of left sidebar)
3. Click **"Database"** tab
4. Find **"Connection string"** section
5. Select **"Transaction"** mode
6. Copy the string

---

## What It Should Look Like

```
postgresql://postgres.djeyzevh:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

Where:
- `djeyzevh` = your project reference ID
- `[YOUR-PASSWORD]` = the password you set when creating the project
- The rest is the Supabase server address

---

## Important Notes

✅ **Use Transaction mode** - This is correct for SQLAlchemy/FastAPI
❌ **Don't use Session mode** - That's for direct connections

✅ **The password** is the one you set when creating the project
- If you forgot it, you can reset it: Settings → Database → Reset Database Password

---

## Quick Check

Your connection string should:
- ✅ Start with `postgresql://`
- ✅ Contain `pooler.supabase.com`
- ✅ Have your password (the part after the colon in `postgres.djeyzevh:password`)
- ✅ End with `/postgres`
- ✅ Be in **Transaction** mode (not Session)

---

## If You Can't Find It

1. Make sure you're looking at **Database** settings (not API settings)
2. Scroll down on the Database page - it's usually below the connection info
3. The connection string section has a copy button next to it

---

## Next Steps

Once you have the connection string:
1. Add it to your `backend/.env` file as `DATABASE_URL=...`
2. Run `python verify_supabase.py` to test
3. Your tables will auto-create on first backend start




