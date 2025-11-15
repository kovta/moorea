# 🔧 Fix: Missing https:// in REACT_APP_API_URL

## The Problem

Your `REACT_APP_API_URL` in Vercel is missing the `https://` protocol!

**Current (Wrong):**
```
moorea-production.up.railway.app
```

**Should be:**
```
https://moorea-production.up.railway.app
```

---

## ✅ Quick Fix

1. **Vercel Dashboard** → Your project → Settings → Environment Variables
2. **Find `REACT_APP_API_URL`**
3. **Click the edit/pencil icon**
4. **Change the value to:**
   ```
   https://moorea-production.up.railway.app
   ```
   (Add `https://` at the beginning!)
5. **Click "Save"**
6. **Redeploy Vercel:**
   - Deployments → "..." → "Redeploy"
   - Wait 2-5 minutes

---

## 🧪 After Fix

1. **Visit:** `https://mooreamood.com/waitlist`
2. **Open console** (F12)
3. **Check log:** Should show:
   ```
   REACT_APP_API_URL: https://moorea-production.up.railway.app
   API_BASE: https://moorea-production.up.railway.app/api/v1
   ```
4. **Try to sign up** - should work! ✅

---

**The missing `https://` is causing the 405 error!** Fix it and redeploy! 🚀



