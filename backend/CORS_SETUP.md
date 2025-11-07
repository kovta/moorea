# 🔒 CORS Configuration Guide

## What is CORS?

CORS (Cross-Origin Resource Sharing) allows your frontend (on Vercel) to make requests to your backend (on Railway) when they're on different domains.

**Example:**
- Frontend: `https://mooreamood.com` (Vercel)
- Backend: `https://moorea-production.up.railway.app` (Railway)
- ✅ CORS allows these to communicate

---

## ✅ Current Configuration

The backend is now configured to:
- ✅ Read allowed origins from `ALLOWED_ORIGINS` environment variable
- ✅ Support multiple origins (comma-separated)
- ✅ Use secure defaults (no wildcard "*" in production)
- ✅ Allow credentials (cookies, auth tokens)
- ✅ Log which origins are configured

---

## 🚀 Setup for Production

### Step 1: Set ALLOWED_ORIGINS in Railway

1. **Go to Railway Dashboard** → Your service → "Variables" tab
2. **Add/Update this variable:**

   **Name:** `ALLOWED_ORIGINS`
   
   **Value:** (comma-separated list, no spaces after commas)
   ```
   https://mooreamood.com,https://www.mooreamood.com,https://mooreamood.vercel.app
   ```

   **Include:**
   - Your custom domain: `https://mooreamood.com`
   - WWW version: `https://www.mooreamood.com`
   - Vercel preview URL: `https://mooreamood.vercel.app` (optional, for previews)

3. **Save** - Railway will automatically redeploy

---

## 🧪 Testing CORS

### Test 1: Check Backend Logs

After setting `ALLOWED_ORIGINS`, check Railway logs. You should see:
```
CORS configured for production origins: ['https://mooreamood.com', 'https://www.mooreamood.com']
```

If you see a warning instead:
```
⚠️  ALLOWED_ORIGINS not set - using development defaults
```
→ You need to set the environment variable!

### Test 2: Test from Browser Console

1. Visit your frontend: `https://mooreamood.com`
2. Open browser console (F12)
3. Run this:
   ```javascript
   fetch('https://your-railway-url.railway.app/api/v1/waitlist/subscribe', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({ email: 'test@example.com' })
   })
   .then(r => r.json())
   .then(console.log)
   .catch(console.error)
   ```

**✅ Success:** Should return JSON response
**❌ CORS Error:** If you see "CORS policy" error, check:
- `ALLOWED_ORIGINS` is set correctly in Railway
- Frontend URL matches exactly (including `https://` and no trailing slash)
- Railway service has been redeployed after setting the variable

### Test 3: Test Waitlist Form

1. Visit your landing page
2. Fill out the waitlist form
3. Submit
4. **Check browser console** for errors
5. **Check Network tab** → Look for OPTIONS request (preflight)
   - Should return `200 OK`
   - Should have `Access-Control-Allow-Origin` header

---

## 🔍 Troubleshooting CORS Errors

### Error: "Access to fetch blocked by CORS policy"

**Causes:**
1. ❌ `ALLOWED_ORIGINS` not set in Railway
2. ❌ Frontend URL doesn't match exactly (typo, http vs https, trailing slash)
3. ❌ Railway hasn't redeployed after setting variable

**Fix:**
1. Check Railway → Variables → `ALLOWED_ORIGINS`
2. Verify the URL matches exactly (case-sensitive, include protocol)
3. Redeploy Railway service (or wait for auto-redeploy)

### Error: "Credentials flag is true, but Access-Control-Allow-Credentials is not 'true'"

**Cause:** Backend not allowing credentials

**Fix:** Already configured ✅ - `allow_credentials=True` is set

### Error: "Preflight request doesn't pass"

**Cause:** OPTIONS request failing

**Fix:** Already configured ✅ - `allow_methods` includes "OPTIONS"

---

## 📋 CORS Checklist

Before going live, verify:

- [ ] `ALLOWED_ORIGINS` is set in Railway
- [ ] Includes your custom domain: `https://mooreamood.com`
- [ ] Includes www version: `https://www.mooreamood.com`
- [ ] No trailing slashes in URLs
- [ ] Uses `https://` (not `http://`)
- [ ] Railway logs show: "CORS configured for production origins"
- [ ] Test waitlist form works from production site
- [ ] No CORS errors in browser console

---

## 🔐 Security Notes

### ✅ Secure Configuration
- **Specific origins only** - No wildcard "*" in production
- **Credentials allowed** - For auth tokens/cookies
- **Explicit methods** - Only necessary HTTP methods

### ⚠️ Development vs Production

**Development (localhost):**
- Automatically allows `http://localhost:3000`
- No environment variable needed
- Logs a warning if `ALLOWED_ORIGINS` not set

**Production:**
- **MUST** set `ALLOWED_ORIGINS` environment variable
- Only specified origins are allowed
- More secure, prevents unauthorized access

---

## 🎯 Quick Reference

**Railway Environment Variable:**
```
ALLOWED_ORIGINS=https://mooreamood.com,https://www.mooreamood.com
```

**Backend Code Location:**
- `backend/app/main.py` (lines 64-95)

**Frontend API Configuration:**
- `frontend/src/utils/api.ts` (uses `REACT_APP_API_URL`)

---

## ✅ After Setup

Once `ALLOWED_ORIGINS` is set:

1. ✅ Railway will auto-redeploy
2. ✅ Check logs for "CORS configured for production origins"
3. ✅ Test waitlist form from your live site
4. ✅ Verify no CORS errors in browser console

**You're all set! 🚀**

