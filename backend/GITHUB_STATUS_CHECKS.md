# 🔍 Understanding GitHub Status Checks

## What You're Seeing

When you push to GitHub, Railway automatically tries to deploy your services. GitHub shows the status of these deployments as "checks".

### Status Types:
- ✅ **Passing** (Green checkmark) = Deployment succeeded
- ❌ **Failing** (Red X) = Deployment failed
- ⏳ **Pending** (Yellow dot) = Currently deploying

---

## Your Current Status

**2 Failing:**
- `secure-amazement - moorea` - Deployment failed
- `serene-grace - moorea` - Deployment failed

**1 Pending:**
- `spectacular-mercy - moorea` - Currently deploying

---

## 🔍 How to Check Why They Failed

### Option 1: Click "Details" in GitHub

1. **In GitHub**, click the blue **"Details"** link next to each failed check
2. **This opens Railway** and shows you:
   - Build logs (what happened during build)
   - Deploy logs (what happened during deployment)
   - Error messages

### Option 2: Check Railway Dashboard Directly

1. **Go to Railway**: https://railway.app
2. **Click on each service**:
   - `secure-amazement`
   - `serene-grace`
   - `spectacular-mercy`
3. **Check "Deployments" tab**:
   - Look for the latest deployment
   - Click on it to see logs
4. **Check "Logs" tab**:
   - See real-time logs
   - Look for error messages

---

## 🐛 Common Failure Reasons

### 1. Build Failed
**Symptoms:**
- Error in "Build Logs"
- Usually happens during `pip install` or build process

**Common Causes:**
- Missing dependencies in `requirements.txt`
- Python version mismatch
- Large packages timing out (torch, torchvision)
- Missing `git` for CLIP installation

**Fix:**
- Check build logs for specific error
- Update `requirements.txt` or `nixpacks.toml`
- See `RAILWAY_CRASH_FIXES.md` for details

---

### 2. Deployment Failed (Runtime Error)
**Symptoms:**
- Build succeeds, but deployment fails
- Error in "Deploy Logs"
- Service crashes on startup

**Common Causes:**
- Missing `DATABASE_URL` environment variable
- Database connection errors
- Import errors (circular imports, missing modules)
- Memory issues (ML models too large)
- Port binding issues

**Fix:**
- Check deploy logs for specific error
- Verify environment variables are set
- Check `RAILWAY_CRASH_FIXES.md` for solutions

---

### 3. Service Crashed After Start
**Symptoms:**
- Deployment succeeds initially
- Service crashes after running for a while
- Railway keeps restarting

**Common Causes:**
- Database connection exhaustion
- Memory issues (OOM - Out of Memory)
- Stale database connections
- Missing error handling

**Fix:**
- Check Railway logs for crash reason
- See `RAILWAY_CRASH_FIXES.md` for fixes
- Connection pooling is already fixed in code

---

## 🔧 Quick Fixes

### If Build Failed:

1. **Check Build Logs** in Railway
2. **Look for specific error** (e.g., "Could not find torch==2.1.0")
3. **Fix the issue**:
   - Update `requirements.txt`
   - Update `nixpacks.toml`
   - Fix Python version
4. **Push again** → Railway will retry

---

### If Deployment Failed:

1. **Check Deploy Logs** in Railway
2. **Look for startup errors**:
   - `ImportError: cannot import name...`
   - `psycopg2.OperationalError: connection refused`
   - `AttributeError: 'FieldInfo' object...`
3. **Fix the issue**:
   - Add missing environment variables
   - Fix import errors
   - Check database connection
4. **Push again** → Railway will retry

---

### If Service Crashed:

1. **Check Railway Logs** (not build/deploy logs)
2. **Look for runtime errors**:
   - Database connection errors
   - Memory errors
   - Unhandled exceptions
3. **Fix the issue**:
   - Connection pooling (already fixed)
   - Add error handling
   - Disable ML features if memory issue
4. **Service will auto-restart** or push again

---

## 📋 Step-by-Step: Check Failed Deployment

### Step 1: Open Railway Dashboard
1. Go to https://railway.app
2. Log in
3. Find your project

### Step 2: Check Each Service

For each failed service (`secure-amazement`, `serene-grace`):

1. **Click on the service name**
2. **Go to "Deployments" tab**
3. **Click on the latest deployment** (should show ❌ Failed)
4. **Check "Build Logs"**:
   - Scroll to bottom
   - Look for red error messages
   - Common: `ERROR:`, `FAILED:`, `Exception:`
5. **Check "Deploy Logs"**:
   - Look for startup errors
   - Common: `ImportError`, `ConnectionError`, `AttributeError`

### Step 3: Identify the Error

**Look for these patterns:**

```
ERROR: Could not find a version that satisfies the requirement...
→ Missing or wrong package version

ImportError: cannot import name 'X' from 'Y'
→ Circular import or missing module

psycopg2.OperationalError: connection refused
→ DATABASE_URL not set or wrong

AttributeError: 'FieldInfo' object has no attribute...
→ FastAPI/Pydantic version mismatch

Out of Memory (OOM)
→ ML models too large, need more memory
```

### Step 4: Fix and Redeploy

1. **Fix the error** (update code, add env var, etc.)
2. **Commit and push**:
   ```bash
   git add .
   git commit -m "Fix Railway deployment error"
   git push origin main
   ```
3. **Railway will automatically retry** deployment
4. **Check GitHub status** - should turn green ✅

---

## 🎯 What to Do Right Now

### Immediate Actions:

1. **Click "Details" in GitHub** for each failed check
   - This shows you the exact error
   - Or go directly to Railway dashboard

2. **Check Railway Logs**:
   - Railway → Each service → Logs tab
   - Look for error messages

3. **Check Environment Variables**:
   - Railway → Each service → Variables tab
   - Make sure `DATABASE_URL` is set
   - Make sure `ALLOWED_ORIGINS` is set (if needed)

4. **Wait for Pending Deployment**:
   - `spectacular-mercy` is still deploying
   - Wait 2-5 minutes
   - Check if it succeeds or fails

---

## 💡 Pro Tips

1. **One Service Failing is OK**: If you only need one service (e.g., `spectacular-mercy`), you can ignore the others
2. **Check Logs First**: Always check logs before making changes
3. **Common Fix**: Most failures are due to missing `DATABASE_URL` or import errors
4. **Auto-Retry**: Railway will automatically retry when you push new code

---

## ✅ Success Indicators

You'll know it's working when:

- ✅ All GitHub checks show green checkmarks
- ✅ Railway services show "Active" status
- ✅ You can visit `/health` endpoint and get response
- ✅ No errors in Railway logs

---

## 🆘 Still Stuck?

1. **Share the error message** from Railway logs
2. **Check which service you actually need** (maybe you only need one?)
3. **Consider disabling ML features** if only using waitlist (saves memory)

---

## 📊 Service Names Explained

Railway generates random names for services:
- `secure-amazement` = One of your Railway services
- `serene-grace` = Another Railway service
- `spectacular-mercy` = Your main service (currently deploying)

**You might only need one of these!** Check which one is your main backend service.

