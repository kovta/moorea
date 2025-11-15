# 🔧 Railway Multiple Services - Environment Variables

## The Problem

You have multiple Railway services (`serene-grace`, `secure-amazement`, `spectacular-mercy`), and **each service needs its own environment variables**.

**Environment variables are NOT shared between services!**

---

## ✅ Solution: Set DATABASE_URL for Each Service

### For `serene-grace` Service:

1. **Railway Dashboard** → Click on `serene-grace` service
2. **Click "Variables" tab**
3. **Check if `DATABASE_URL` exists**:
   - If **NO** → Add it (see steps below)
   - If **YES** → Check the value is correct

### To Add DATABASE_URL:

1. **Click "New Variable"**
2. **Name**: `DATABASE_URL`
3. **Value**: Your Supabase connection string
   ```
   postgresql://postgres.djezqevhrdygxkhskflw:[YOUR-PASSWORD]@aws-1-eu-north-1.pooler.supabase.com:6543/postgres
   ```
   (Replace `[YOUR-PASSWORD]` with your actual password)
4. **Click "Add"**
5. **Railway will auto-redeploy**

---

## 📋 Checklist: Set Variables for ALL Services

You need to set `DATABASE_URL` in **each service**:

- [ ] `serene-grace` → Variables → `DATABASE_URL` set
- [ ] `secure-amazement` → Variables → `DATABASE_URL` set  
- [ ] `spectacular-mercy` → Variables → `DATABASE_URL` set

**Each service is independent!** Setting it in one doesn't set it in others.

---

## 🔍 How to Verify It's Set

After adding `DATABASE_URL`, check the logs. You should see:

**✅ Good:**
```
🔗 Database URL: postgresql://postgres.djezqevhrdygxkhskflw:****@aws-1-eu-north-1.pooler.supabase.com:6543/postgres
Database tables created
```

**❌ Bad (what you're seeing now):**
```
🔗 Database URL: postgresql:****@localhost/moorea
⚠️  WARNING: Using localhost fallback - DATABASE_URL not set in environment!
```

---

## 💡 Pro Tip: Copy Variables Between Services

If you've already set `DATABASE_URL` in one service:

1. **Go to the service that has it** (e.g., `spectacular-mercy`)
2. **Variables tab** → Find `DATABASE_URL`
3. **Click on the value** to copy it (password is masked, but you can copy the structure)
4. **Go to the other service** (e.g., `serene-grace`)
5. **Add the same variable** with the same value

---

## 🎯 Quick Fix Right Now

**For `serene-grace` service:**

1. Railway → `serene-grace` → Variables
2. Add `DATABASE_URL` with your Supabase connection string
3. Wait for redeploy (2-3 minutes)
4. Check logs - should work! ✅

---

## ⚠️ Important Notes

1. **Each service = separate environment**
   - Variables set in `spectacular-mercy` don't apply to `serene-grace`
   - You must set them in each service individually

2. **Root Directory is also per-service**
   - Make sure each service has Root Directory set to `backend`

3. **You might only need one service**
   - If `spectacular-mercy` is working, you might not need the others
   - Consider deleting unused services to avoid confusion

---

## 🚀 After Setting DATABASE_URL

Once you set `DATABASE_URL` in `serene-grace`:

1. Railway will automatically redeploy
2. Check logs - should see "Database tables created"
3. Service should start successfully ✅
4. GitHub status check should turn green ✅

---

**The key issue: `DATABASE_URL` is not set in the `serene-grace` service, even though it might be set in other services!**

