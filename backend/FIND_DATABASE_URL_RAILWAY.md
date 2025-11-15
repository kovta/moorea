# 🔍 How to Find DATABASE_URL in Railway

## Step-by-Step Guide

### Step 1: Go to Railway Dashboard
1. **Open**: https://railway.app
2. **Log in** to your account

---

### Step 2: Select Your Project
1. **Click on your project** (e.g., "moorea" or your project name)
2. You'll see a list of services

---

### Step 3: Select Your Service
1. **Click on the service** you want to check (e.g., `spectacular-mercy`, `secure-amazement`, or `serene-grace`)
2. This opens the service dashboard

---

### Step 4: Go to Variables Tab
1. **Look at the top menu** in the service dashboard
2. **Click on "Variables"** tab
   - It's usually next to "Settings", "Deployments", "Logs", etc.
   - The icon might look like a list or settings icon

---

### Step 5: Find DATABASE_URL
1. **Scroll through the list** of environment variables
2. **Look for `DATABASE_URL`** in the list
3. **You'll see**:
   - **Name**: `DATABASE_URL`
   - **Value**: Your connection string (password is hidden/masked)

---

## 📸 What You'll See

### If DATABASE_URL is Set ✅:
```
Name: DATABASE_URL
Value: postgresql://postgres.djezqevhrdygxkhskflw:****@aws-1-eu-north-1.pooler.supabase.com:6543/postgres
```
- The password is masked with `****` for security
- You can see the host, port, and database name

### If DATABASE_URL is NOT Set ❌:
- You won't see `DATABASE_URL` in the list at all
- Or you'll see it with an empty value

---

## ➕ How to Add DATABASE_URL (If Missing)

### Step 1: Get Your Supabase Connection String
1. **Go to Supabase**: https://supabase.com/dashboard
2. **Select your project**
3. **Click Settings** (⚙️) → **Database**
4. **Scroll to "Connection string"**
5. **Select "Transaction" mode** (under Connection pooling)
6. **Copy the connection string**
7. **Replace `[YOUR-PASSWORD]`** with your actual password

### Step 2: Add to Railway
1. **In Railway** → Your service → **Variables** tab
2. **Click "New Variable"** button (usually top right)
3. **Enter**:
   - **Variable Name**: `DATABASE_URL`
   - **Value**: Paste your connection string (with password)
4. **Click "Add"** or "Save"
5. **Railway will automatically redeploy**

---

## 🔍 Alternative: Check in Settings

Some Railway interfaces show variables in:
- **Settings** → **Variables** (instead of a separate Variables tab)
- **Environment** → **Variables**

**Look for these tabs if you don't see "Variables"**

---

## ✅ Quick Checklist

To verify DATABASE_URL is set correctly:

- [ ] Go to Railway → Your service
- [ ] Click "Variables" tab
- [ ] See `DATABASE_URL` in the list
- [ ] Value shows your Supabase connection string (password masked)
- [ ] Connection string includes: `pooler.supabase.com` (for pooled connection)

---

## 🎯 Visual Guide

**Railway Dashboard Structure:**
```
Railway Dashboard
  └── Your Project
      └── Your Service (e.g., spectacular-mercy)
          ├── Deployments (tab)
          ├── Logs (tab)
          ├── Variables (tab) ← CLICK HERE
          ├── Settings (tab)
          └── Metrics (tab)
```

**Variables Tab:**
```
Variables
├── DATABASE_URL: postgresql://...****@...supabase.com:6543/postgres
├── SECRET_KEY: your-secret-key
├── ALLOWED_ORIGINS: https://mooreamood.com,https://www.mooreamood.com
└── [New Variable] button
```

---

## 💡 Pro Tips

1. **Password is Hidden**: Railway masks passwords in the UI for security
2. **Check All Services**: If you have multiple services, check each one
3. **Copy Value**: You can click on the value to copy it (but password stays masked)
4. **Auto-Redeploy**: When you add/update a variable, Railway automatically redeploys

---

## 🚨 If You Don't See DATABASE_URL

**It's not set!** You need to add it:

1. **Get connection string** from Supabase (see steps above)
2. **Add it to Railway** → Variables → New Variable
3. **Wait for redeploy** (2-3 minutes)
4. **Check logs** - should see "Database tables created"

---

## 🔗 Related Files

- `RAILWAY_DATABASE_SETUP.md` - Complete setup guide
- `SUPABASE_SETUP.md` - How to get connection string from Supabase

