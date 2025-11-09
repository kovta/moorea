# 🚨 URGENT: Set DATABASE_URL in Railway

## The Problem

Your Railway deployment is crashing because `DATABASE_URL` is not set, so it's trying to connect to `localhost` (which doesn't exist in Railway).

**Error you're seeing:**
```
connection to server at "localhost" (::1), port 5432 failed: Connection refused
```

## ✅ Quick Fix (2 minutes)

### Step 1: Get Your Supabase Connection String

1. **Go to Supabase Dashboard**: https://supabase.com/dashboard
2. **Select your project** (moorea-backend or similar)
3. **Click Settings** (⚙️ gear icon) → **Database**
4. **Scroll to "Connection string"** section
5. **Under "Connection pooling"**, select **"Transaction" mode**
6. **Copy the connection string** - it looks like:
   ```
   postgresql://postgres.djezqevhrdygxkhskflw:[YOUR-PASSWORD]@aws-1-eu-north-1.pooler.supabase.com:6543/postgres
   ```
7. **Replace `[YOUR-PASSWORD]`** with your actual Supabase database password

### Step 2: Add to Railway

1. **Go to Railway Dashboard**: https://railway.app
2. **Click on your service** (moorea)
3. **Click "Variables" tab**
4. **Click "New Variable"**
5. **Add:**
   - **Name:** `DATABASE_URL`
   - **Value:** Paste your Supabase connection string (with password replaced)
6. **Click "Add"**
7. **Railway will automatically redeploy**

### Step 3: Verify

1. **Wait 2-3 minutes** for Railway to redeploy
2. **Check Railway Logs** - you should see:
   - `🔗 Database URL: postgresql://postgres.djezqevhrdygxkhskflw:****@aws-1-eu-north-1.pooler.supabase.com:6543/postgres`
   - `Database tables created`
   - `Services initialized successfully`
3. **No more localhost errors!**

---

## 📋 Complete Environment Variables Checklist

Make sure these are set in Railway → Variables:

### ✅ Required:
- [ ] `DATABASE_URL` - Your Supabase connection string (Transaction mode)
- [ ] `SECRET_KEY` - Any random string (for JWT tokens)

### ✅ Recommended:
- [ ] `ALLOWED_ORIGINS` - Your frontend URL (e.g., `https://mooreamood.com,https://www.mooreamood.com`)

### ⚠️ Optional (only if using ML features):
- API keys (Unsplash, Pexels, etc.)

---

## 🔍 How to Verify It's Set

After adding `DATABASE_URL`, check Railway logs. You should see:

**✅ Good:**
```
🔗 Database URL: postgresql://postgres.djezqevhrdygxkhskflw:****@aws-1-eu-north-1.pooler.supabase.com:6543/postgres
Database tables created
```

**❌ Bad (if you see this, DATABASE_URL is still not set):**
```
⚠️  WARNING: Using localhost fallback - DATABASE_URL not set in environment!
```

---

## 🎯 Quick Steps Summary

1. Get Supabase connection string (Transaction mode)
2. Railway → Your service → Variables → New Variable
3. Name: `DATABASE_URL`
4. Value: Your connection string (with password)
5. Save
6. Wait for redeploy
7. Check logs - should work! ✅

---

## 💡 Pro Tip

**Don't forget the password!** The connection string has `[YOUR-PASSWORD]` placeholder - replace it with your actual Supabase database password.

If you forgot your password:
- Supabase Dashboard → Settings → Database → Reset Database Password

---

**Once you set `DATABASE_URL`, the app should start successfully!** 🚀

