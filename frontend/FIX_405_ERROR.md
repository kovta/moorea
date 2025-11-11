# 🔧 Fix 405 Error on Waitlist Signup

## The Problem

**Error:** `Request failed with status code 405`

**Meaning:** "Method Not Allowed" - The HTTP method (POST) is not allowed for this endpoint, or the endpoint doesn't exist.

---

## 🔍 Root Cause Analysis

### Frontend API Call:
- **File:** `frontend/src/utils/api.ts`
- **Function:** `subscribeToWaitlist()`
- **Endpoint:** `/waitlist/subscribe`
- **Method:** `POST`
- **Full URL:** `{API_BASE}/waitlist/subscribe`
- **API_BASE:** `process.env.REACT_APP_API_URL || '/api/v1'`

### Backend Route:
- **File:** `backend/app/routes/waitlist.py`
- **Router prefix:** `/api/v1/waitlist`
- **Route:** `/subscribe`
- **Method:** `POST`
- **Full path:** `/api/v1/waitlist/subscribe`

### Expected Full URL:
- If `REACT_APP_API_URL` is set: `{REACT_APP_API_URL}/waitlist/subscribe`
- If not set (defaults): `/api/v1/waitlist/subscribe`

**Problem:** The frontend is calling `/waitlist/subscribe` but needs `/api/v1/waitlist/subscribe`!

---

## ✅ Solution

### Option 1: Fix API_BASE in Frontend (Recommended)

The frontend should use the full path including `/api/v1`:

**Current code:**
```typescript
const API_BASE = process.env.REACT_APP_API_URL || '/api/v1';
// ...
apiClient.post('/waitlist/subscribe', ...)  // This becomes /api/v1/waitlist/subscribe ✅
```

Actually, this should work! The issue might be:

### Option 2: Check REACT_APP_API_URL in Vercel

**The problem might be:**
- `REACT_APP_API_URL` is set incorrectly in Vercel
- It might be set to just the base URL without `/api/v1`
- Or it might be missing entirely

**Check in Vercel:**
1. Vercel Dashboard → Your project → Settings → Environment Variables
2. Find `REACT_APP_API_URL`
3. **Should be:** `https://your-railway-url.railway.app` (without trailing slash)
4. **NOT:** `https://your-railway-url.railway.app/api/v1` (the code adds this)

**If missing or wrong:**
- Add/Update: `REACT_APP_API_URL` = `https://your-railway-service.railway.app`
- Redeploy Vercel

---

## 🔍 Debugging Steps

### Step 1: Check Browser Console

When you try to sign up, check the browser console (F12) and look for:
- The actual URL being called
- Any CORS errors
- The full error message

### Step 2: Check Network Tab

1. Open browser DevTools (F12)
2. Go to "Network" tab
3. Try to sign up
4. Look for the failed request
5. Check:
   - **Request URL:** What's the full URL?
   - **Request Method:** Should be `POST`
   - **Status:** Should show `405`
   - **Request Headers:** Check if `Content-Type: application/json` is set

### Step 3: Verify Backend is Running

1. Check Railway Dashboard
2. Service should be "Active"
3. Test the endpoint directly:
   ```bash
   curl -X POST https://your-railway-url.railway.app/api/v1/waitlist/subscribe \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","name":"Test"}'
   ```

---

## 🐛 Common Causes of 405 Error

1. **Wrong HTTP Method**
   - Frontend using GET instead of POST
   - ✅ Already using POST - not this issue

2. **Wrong Endpoint Path**
   - URL doesn't match backend route
   - **Possible issue:** API_BASE configuration

3. **CORS Preflight Failure**
   - OPTIONS request fails, causing 405
   - Check `ALLOWED_ORIGINS` in Railway

4. **Backend Route Not Registered**
   - Router not included in main.py
   - ✅ Already included - not this issue

---

## ✅ Quick Fix Checklist

- [ ] Check `REACT_APP_API_URL` in Vercel Environment Variables
- [ ] Should be: `https://your-railway-url.railway.app` (no trailing slash, no `/api/v1`)
- [ ] Verify Railway service is running and accessible
- [ ] Check `ALLOWED_ORIGINS` in Railway includes your Vercel domain
- [ ] Test backend endpoint directly with curl
- [ ] Check browser Network tab for actual request URL
- [ ] Redeploy Vercel after fixing environment variable

---

## 🧪 Test After Fix

1. **Set `REACT_APP_API_URL`** in Vercel (if not set)
2. **Redeploy Vercel** (or wait for auto-deploy)
3. **Visit:** `https://mooreamood.com/waitlist`
4. **Try to sign up**
5. **Should work!** ✅

---

## 📋 Expected Behavior

**Before fix:**
- Error: `405 Method Not Allowed`
- Request fails

**After fix:**
- Success message: "Successfully added to waitlist!"
- Email saved to database
- Form clears

---

**The most likely issue is `REACT_APP_API_URL` not being set correctly in Vercel!** 🎯

