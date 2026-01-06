# ⚙️ Vercel Configuration for React Router

## ✅ What We Already Have

**`vercel.json` file** (in `frontend/` folder):
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

This tells Vercel to serve `index.html` for all routes, allowing React Router to handle routing.

---

## 🔍 Vercel Dashboard Settings to Check

### 1. Root Directory (CRITICAL!)

**Location:** Vercel → Your Project → Settings → General

**Must be set to:** `frontend`

**Why:** Vercel needs to know where your `vercel.json` and `package.json` are.

**How to check:**
1. Vercel Dashboard → Your project
2. Settings → General
3. Look for "Root Directory"
4. Should say: `frontend`
5. If blank or wrong → Click "Edit" → Set to `frontend` → Save

---

### 2. Framework Preset

**Location:** Vercel → Your Project → Settings → General → Build & Development Settings

**Should be:** `Create React App` or `React`

**Why:** Vercel needs to know how to build your app.

**How to check:**
1. Vercel Dashboard → Your project
2. Settings → General
3. Scroll to "Build & Development Settings"
4. Check "Framework Preset"
5. Should be: `Create React App` or `React`

---

### 3. Build Command

**Location:** Same as above

**Should be:** `npm run build` (or leave default)

**How to check:**
1. Same location as Framework Preset
2. Check "Build Command"
3. Should be: `npm run build`

---

### 4. Output Directory

**Location:** Same as above

**Should be:** `build`

**Why:** This is where React builds your app.

**How to check:**
1. Same location
2. Check "Output Directory"
3. Should be: `build`

---

### 5. Install Command

**Location:** Same as above

**Should be:** `npm install` (or leave default)

---

## 🔍 Verify vercel.json is Being Read

### Check 1: File Location

The `vercel.json` file **must** be in the `frontend/` folder (same level as `package.json`).

**Current location:** ✅ `/frontend/vercel.json` (correct!)

### Check 2: Vercel Detects It

Vercel should automatically detect `vercel.json` if:
- ✅ Root Directory is set to `frontend`
- ✅ File is in the `frontend/` folder
- ✅ File has valid JSON syntax

**How to verify:**
1. Vercel Dashboard → Your project → Deployments
2. Click on a deployment
3. Check "Build Logs"
4. Look for: "Detected vercel.json" or similar message

---

## 🐛 If Routes Still Don't Work

### Problem: "No routes matched location '/waitlist'"

**Possible causes:**

1. **vercel.json not in Root Directory**
   - If Root Directory is `frontend`, vercel.json must be in `frontend/`
   - ✅ Already correct!

2. **Old deployment**
   - Latest code hasn't been deployed yet
   - **Fix:** Wait for auto-deploy or manually redeploy

3. **Build output doesn't include routes**
   - React build might be failing
   - **Fix:** Check Build Logs in Vercel

4. **vercel.json syntax error**
   - Invalid JSON
   - **Fix:** Validate JSON syntax

---

## ✅ Complete Checklist

Before reporting issues, verify:

- [ ] `vercel.json` exists in `frontend/` folder
- [ ] `vercel.json` has valid JSON syntax
- [ ] Root Directory is set to `frontend` in Vercel
- [ ] Framework Preset is `Create React App` or `React`
- [ ] Output Directory is `build`
- [ ] Latest code is deployed (check Deployments tab)
- [ ] Build succeeded (green checkmark in Deployments)

---

## 🧪 Test Configuration

### Test 1: Check vercel.json is Deployed

1. Visit: `https://mooreamood.com/vercel.json` (or your Vercel URL)
2. Should return: `404` or redirect (this is normal - vercel.json is config, not a route)
3. If you see the JSON content, that's also fine

### Test 2: Test Routes

1. Visit: `https://mooreamood.com/` → Should show Home page
2. Visit: `https://mooreamood.com/waitlist` → Should show Waitlist page
3. Visit: `https://mooreamood.com/nonexistent` → Should show Home page (catch-all)

**If `/waitlist` shows 404:**
- vercel.json rewrite isn't working
- Check Root Directory setting
- Redeploy

---

## 💡 Important Notes

1. **vercel.json must be in Root Directory**
   - If Root Directory = `frontend`, then vercel.json must be in `frontend/`
   - ✅ We already have this!

2. **Vercel reads vercel.json automatically**
   - No need to configure it in dashboard
   - Just make sure Root Directory is correct

3. **Rewrites vs Redirects**
   - We use **rewrites** (keeps URL, serves different file)
   - Not redirects (changes URL)
   - ✅ Our config is correct!

---

## 🚀 Quick Fix Summary

**If routes aren't working:**

1. **Check Root Directory** in Vercel → Settings → General
   - Must be: `frontend`
   
2. **Verify vercel.json exists** in `frontend/` folder
   - ✅ Already there!

3. **Redeploy** (wait for auto-deploy or manually trigger)
   - Vercel needs to rebuild with latest code

4. **Check Build Logs**
   - Should see successful build
   - No errors about vercel.json

---

## 📋 Current Status

✅ **vercel.json** is correctly configured
✅ **File location** is correct (`frontend/vercel.json`)
✅ **JSON syntax** is valid

**What to check in Vercel Dashboard:**
- Root Directory = `frontend`
- Framework Preset = `Create React App` or `React`
- Latest deployment succeeded

**If all above are correct, routes should work after redeploy!** 🚀

