# 🐛 Debug 405 Error - Step by Step

## Current Status

✅ `REACT_APP_API_URL` is set in Vercel
❌ Still getting 405 error

---

## 🔍 Step 1: Check Browser Console

1. **Visit:** `https://mooreamood.com/waitlist`
2. **Open browser console** (F12)
3. **Look for the log:**
   ```
   🔧 Environment check: { ... }
   ```
4. **Check what it shows:**
   - `REACT_APP_API_URL`: Should be your Railway URL
   - `API_BASE`: Should be `{Railway URL}/api/v1`

**Share what you see in the console!**

---

## 🔍 Step 2: Check Network Tab

1. **Open browser DevTools** (F12)
2. **Go to "Network" tab**
3. **Try to sign up** (fill form and submit)
4. **Look for the failed request:**
   - Find the request to `/waitlist/subscribe` or similar
   - Click on it
   - Check:
     - **Request URL:** What's the full URL?
     - **Request Method:** Should be `POST`
     - **Status Code:** Should show `405`
     - **Request Headers:** Check `Content-Type: application/json`

**Share the Request URL you see!**

---

## 🔍 Step 3: Check if Vercel Redeployed

1. **Vercel Dashboard** → Your project → **Deployments**
2. **Check latest deployment:**
   - Is it from **after** you added `REACT_APP_API_URL`?
   - Does it show **✅ Success**?
3. **If deployment is old:**
   - Click "..." → "Redeploy"
   - Wait 2-5 minutes

---

## 🔍 Step 4: Test Backend Directly

Test if the backend endpoint works:

**Replace `YOUR_RAILWAY_URL` with your actual Railway URL:**

```bash
curl -X POST https://YOUR_RAILWAY_URL.railway.app/api/v1/waitlist/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"Test"}'
```

**Expected:**
```json
{
  "success": true,
  "message": "Successfully added to waitlist!",
  "email": "test@example.com"
}
```

**If this works:** Backend is fine, issue is with frontend/configuration
**If this fails:** Backend issue (check Railway logs)

---

## 🔍 Step 5: Check CORS

1. **Railway Dashboard** → Your service → **Variables**
2. **Check `ALLOWED_ORIGINS`:**
   - Should include: `https://mooreamood.com`
   - Should include: `https://www.mooreamood.com`
   - Format: `https://mooreamood.com,https://www.mooreamood.com` (comma-separated, no spaces)

**If missing or wrong:**
- Add/Update `ALLOWED_ORIGINS`
- Railway will auto-redeploy
- Wait 2-3 minutes

---

## 🔍 Step 6: Check Railway Service Status

1. **Railway Dashboard** → Your service
2. **Check status:**
   - Should be **"Active"** (green)
   - Not "Crashed" or "Restarting"
3. **Check logs:**
   - Look for errors
   - Should see: "Database tables created"
   - Should see: "Services initialized successfully"

---

## 🎯 Most Likely Issues

1. **Vercel hasn't redeployed yet**
   - Fix: Wait for auto-redeploy or manually redeploy

2. **CORS blocking the request**
   - Fix: Check `ALLOWED_ORIGINS` in Railway

3. **Wrong API URL format**
   - Fix: Should be just `https://railway-url.railway.app` (no trailing slash, no paths)

4. **Backend service not running**
   - Fix: Check Railway service status

---

## 📋 What to Share

To help debug, please share:

1. **Console log** from Step 1 (the `🔧 Environment check:` output)
2. **Request URL** from Step 2 (Network tab)
3. **Result of curl test** from Step 4
4. **Railway service status** (Active/Crashed/etc.)

This will help identify the exact issue! 🔍

