# 🚀 Quick Supabase Setup - Follow These Steps

## Step 1: Create New Project in Supabase

1. **Go to your Supabase Dashboard**: https://supabase.com/dashboard
2. **Click "New Project"** (or the "+" button)
3. **Fill in the details**:
   - **Name**: `moorea-backend` (or any name you like)
   - **Organization**: Create new or use existing
   - **Database Password**: 
     - **⚠️ IMPORTANT**: Generate or create a STRONG password here
     - **SAVE THIS PASSWORD** - Supabase won't show it again!
     - You can use their auto-generator or create your own
   - **Region**: Choose closest to you (e.g., `US East (N. Virginia)`)
4. **Click "Create new project"**
5. **Wait 2-3 minutes** for Supabase to set up your database

---

## Step 2: Get Your Connection String

Once your project is ready:

1. In your Supabase project dashboard, click **Settings** (⚙️ gear icon in left sidebar)
2. Click **Database** in the settings menu
3. Scroll down to **"Connection string"** section
4. **IMPORTANT**: Under **"Connection pooling"**, select **"Transaction" mode**
5. You'll see a connection string that looks like:
   ```
   postgresql://postgres.xxxxx:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```
6. **Copy the ENTIRE connection string** (including the password part)

---

## Step 3: Add to Your .env File

1. Open your `.env` file in the `backend` folder
2. Add or update this line:
   ```bash
   DATABASE_URL=postgresql://postgres.xxxxx:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres
   ```
3. Replace `[YOUR-PASSWORD]` with your actual password from Step 1
4. **Save the file**

---

## Step 4: Verify Connection

Run this command to test:

```bash
cd /Users/kovacstamaspal/dev/moorea/backend
python verify_supabase.py
```

You should see:
```
✅ Database connection successful!
✅ Tables created/verified!
✅ All checks passed!
```

---

## Step 5: Start Your Backend

```bash
python -m uvicorn app.main:app --reload
```

Check the logs - you should see:
```
Database tables created
```

---

## 🆘 Troubleshooting

**"Connection refused" or "authentication failed"**?
- ✅ Check your password is correct (no extra spaces)
- ✅ Make sure you're using **Transaction mode** connection string
- ✅ Verify the connection string is complete

**"Module not found" errors**?
- ✅ Make sure you're in the `backend` directory
- ✅ Install dependencies: `pip install -r requirements.txt`

**Can't find the connection string?**
- ✅ Make sure your project is fully set up (wait 2-3 minutes)
- ✅ Go to Settings → Database (not Settings → General)

---

## ✅ Success Checklist

- [ ] Supabase project created
- [ ] Database password saved
- [ ] Connection string copied (Transaction mode)
- [ ] Added DATABASE_URL to .env file
- [ ] Ran `verify_supabase.py` - all checks passed
- [ ] Backend starts without errors

---

**Once you've done Step 2 (getting the connection string), let me know and I can help you test it!**




