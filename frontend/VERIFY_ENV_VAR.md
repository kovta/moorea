# 🔍 Verify Environment Variable is Working

## The Problem

Even though `REACT_APP_API_URL` is set correctly in Vercel, the request is still going to the wrong URL.

**Error shows:**
```
https://www.mooreamood.com/moorea-production.up.railway.app/api/v1/waitlist/subscribe
```

This means the Railway URL is being treated as a **relative path** instead of an absolute URL.

---

## 🔍 Step 1: Check Browser Console

1. **Visit:** `https://mooreamood.com/waitlist`
2. **Open browser console** (F12)
3. **Look for this log:**
   ```
   🔧 Environment check: { ... }
   ```
4. **Check what it shows:**
   - `REACT_APP_API_URL`: Should be `https://moorea-production.up.railway.app`
   - `API_BASE`: Should be `https://moorea-production.up.railway.app/api/v1`

**What does your console show?** Share this output!

---

## 🔍 Step 2: Check if Variable is Set for Production

1. **Vercel Dashboard** → Your project → Settings → Environment Variables
2. **Find `REACT_APP_API_URL`**
3. **Check which environments it's set for:**
   - Should be checked for **"Production"** ✅
   - Should be checked for **"Preview"** (optional)
   - Should be checked for **"Development"** (optional)

**If "Production" is NOT checked:**
- Click "Edit" on the variable
- Make sure "Production" is checked ✅
- Save
- Redeploy

---

## 🔍 Step 3: Verify Latest Deployment

1. **Vercel Dashboard** → Your project → Deployments
2. **Check latest deployment:**
   - Is it from **after** you set the environment variable?
   - Is it from **after** my latest code fix (commit `1733efc`)?
   - Does it show **✅ Success**?

**If deployment is old:**
- Click "..." → "Redeploy"
- Wait 2-5 minutes

---

## 🔍 Step 4: Check Build Logs

1. **Vercel Dashboard** → Your project → Deployments
2. **Click on latest deployment**
3. **Check "Build Logs"**
4. **Look for:**
   - Environment variables being loaded
   - Any warnings about `REACT_APP_API_URL`
   - Build completion

---

## 🐛 Common Issues

### Issue 1: Variable Not Set for Production
- **Symptom:** Variable exists but not checked for Production
- **Fix:** Edit variable, check "Production", save, redeploy

### Issue 2: Old Deployment
- **Symptom:** Latest deployment is from before setting the variable
- **Fix:** Manually redeploy

### Issue 3: Build Cache
- **Symptom:** Variable is set but old value is still used
- **Fix:** Redeploy with "Clear build cache" option

---

## 📋 What to Share

To help debug, please share:

1. **Console log output** (the `🔧 Environment check:` log)
2. **Which environments** the variable is set for (Production/Preview/Development)
3. **Latest deployment timestamp** (when was it deployed?)
4. **Build logs** (any warnings or errors?)

This will help identify the exact issue! 🔍

