# ✅ Fix REACT_APP_API_URL in Vercel

## The Problem

The `REACT_APP_API_URL` value in Vercel is set to a **comment/instruction** instead of the actual Railway URL.

**Current (Wrong):**
```
- Health check works: Visit `https://your-railway-url.railway.app/health`
```

**Should be:**
```
https://your-actual-railway-url.railway.app
```

---

## ✅ Step-by-Step Fix

### Step 1: Get Your Railway URL

1. **Go to Railway Dashboard**: https://railway.app
2. **Click on your backend service** (e.g., `spectacular-mercy`, `serene-grace`, or whichever is running)
3. **Click "Settings" tab**
4. **Go to "Networking" section**
5. **Find "Public Domain"** or **"Generate Domain"**
6. **Copy the URL** - it looks like:
   ```
   https://your-service-name.up.railway.app
   ```
   **OR**
   ```
   https://your-service-name.railway.app
   ```

**Important:** Copy just the base URL, **NOT** including `/health` or `/api/v1`

---

### Step 2: Update in Vercel

1. **Go to Vercel Dashboard**: https://vercel.com
2. **Click your project**
3. **Settings** → **Environment Variables**
4. **Find `REACT_APP_API_URL`**
5. **Click the edit/pencil icon**
6. **Replace the value with your Railway URL:**
   ```
   https://your-service-name.up.railway.app
   ```
   **Example:**
   ```
   https://spectacular-mercy-production.up.railway.app
   ```
7. **Click "Save"**
8. **Important:** Make sure it's set for **"Production, Preview, and Development"** (or at least Production)

---

### Step 3: Redeploy Vercel

After updating the environment variable:

1. **Go to Deployments tab**
2. **Click "..." on latest deployment**
3. **Click "Redeploy"**
4. **Wait 2-5 minutes** for build to complete

**OR** wait for Vercel to auto-redeploy (may take a few minutes)

---

## ✅ What the Value Should Look Like

**Correct format:**
```
https://spectacular-mercy-production.up.railway.app
```

**NOT:**
- ❌ `https://your-railway-url.railway.app` (placeholder)
- ❌ `https://your-service.railway.app/health` (includes path)
- ❌ `https://your-service.railway.app/api/v1` (includes path)
- ❌ Any text/instructions/comments

**Just the base Railway URL!** The frontend code will automatically add `/api/v1` to it.

---

## 🧪 Verify It's Working

After redeploy:

1. **Visit:** `https://mooreamood.com/waitlist`
2. **Open browser console** (F12)
3. **Look for:** `🔧 Environment check:` log
4. **Should show:**
   ```
   REACT_APP_API_URL: https://your-railway-url.railway.app
   API_BASE: https://your-railway-url.railway.app/api/v1
   ```
5. **Try to sign up** - should work! ✅

---

## 📋 Quick Checklist

- [ ] Got Railway URL from Railway Dashboard → Settings → Networking
- [ ] Updated `REACT_APP_API_URL` in Vercel with just the base URL
- [ ] No trailing slash in the URL
- [ ] No `/health` or `/api/v1` in the URL
- [ ] Set for "Production" environment (at minimum)
- [ ] Redeployed Vercel
- [ ] Tested waitlist signup - works! ✅

---

## 💡 Why This Matters

The frontend code does:
```typescript
API_BASE = REACT_APP_API_URL + '/api/v1'
// Then calls: API_BASE + '/waitlist/subscribe'
```

So if `REACT_APP_API_URL` = `https://your-service.railway.app`
- Full URL becomes: `https://your-service.railway.app/api/v1/waitlist/subscribe` ✅

If it's wrong (like a comment), the request fails with 405 error! ❌

---

**Once you set the correct Railway URL in Vercel and redeploy, the 405 error will be fixed!** 🚀

