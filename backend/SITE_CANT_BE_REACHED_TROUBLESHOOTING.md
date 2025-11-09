# 🔍 "Site Can't Be Reached" - Troubleshooting Guide

## Which Site Can't Be Reached?

### Option 1: Railway Backend (API)
- URL: `https://your-service-name.up.railway.app`
- Error: "This site can't be reached" or "Connection refused"

### Option 2: Frontend (Vercel)
- URL: `https://mooreamood.com` or `https://your-app.vercel.app`
- Error: "This site can't be reached" or "DNS_PROBE_FINISHED_NXDOMAIN"

### Option 3: Custom Domain
- URL: `https://mooreamood.com`
- Error: "This site can't be reached" or DNS errors

---

## 🔧 Fix 1: Railway Service Not Exposed (Most Common!)

### Problem:
Railway services are **private by default**. You need to make them public.

### Solution:

1. **Go to Railway Dashboard** → Your service
2. **Click "Settings" tab**
3. **Go to "Networking" section**
4. **Look for "Public Networking" or "Generate Domain"**
5. **Click "Generate Domain"** or toggle "Public" to ON
6. **Copy the public URL** (e.g., `https://moorea-production.up.railway.app`)

### Verify:
- Visit the URL in your browser
- Should see: `{"status":"healthy","timestamp":"...","version":"1.0.0"}`
- Or visit `/health` endpoint

---

## 🔧 Fix 2: Service is Crashing

### Check Railway Status:

1. **Railway Dashboard** → Your service
2. **Look at the top** - Status should be "Active" (green)
3. **If it says "Crashed" or "Restarting"**:
   - Click "Logs" tab
   - Look for error messages
   - Common issues:
     - Import errors (like the waitlist one we just fixed)
     - Database connection errors
     - Missing environment variables

### Check Recent Deployments:

1. **Railway** → Your service → "Deployments" tab
2. **Look at the latest deployment**:
   - ✅ Green checkmark = Success
   - ❌ Red X = Failed
   - 🔄 Spinning = Still deploying

### If Deployment Failed:

1. **Click on the failed deployment**
2. **Check "Build Logs"** for build errors
3. **Check "Deploy Logs"** for runtime errors
4. **Fix the error** and push again

---

## 🔧 Fix 3: Wrong URL

### Get the Correct Railway URL:

1. **Railway Dashboard** → Your service
2. **Settings** → **Networking**
3. **Copy the exact URL** shown (should end in `.railway.app`)
4. **Test it**: Visit `https://your-url.railway.app/health`

### Common Mistakes:
- ❌ Using `http://` instead of `https://`
- ❌ Missing `.railway.app` domain
- ❌ Using wrong service name
- ❌ Using localhost URL

---

## 🔧 Fix 4: Service Still Deploying

### Check Deployment Status:

1. **Railway** → Your service → "Deployments" tab
2. **Latest deployment status**:
   - "Building" = Still installing dependencies
   - "Deploying" = Starting the app
   - "Active" = Running ✅

### Wait Time:
- First deployment: 5-10 minutes (installing ML packages)
- Subsequent deployments: 2-5 minutes
- If stuck > 15 minutes, check logs for errors

---

## 🔧 Fix 5: Frontend Can't Reach Backend

### Problem:
Frontend (Vercel) can't connect to backend (Railway)

### Check:

1. **Is Railway service public?** (Fix 1 above)
2. **Is `REACT_APP_API_URL` set in Vercel?**
   - Vercel Dashboard → Your project → Settings → Environment Variables
   - Should be: `https://your-railway-url.railway.app`
3. **Is CORS configured?**
   - Railway → Variables → `ALLOWED_ORIGINS`
   - Should include your frontend URL

### Test:

1. **Open browser console** (F12) on your frontend
2. **Look for errors**:
   - CORS errors = CORS not configured
   - Network errors = Backend URL wrong or not accessible
   - Timeout = Backend not running

---

## 🔧 Fix 6: Custom Domain Not Working

### Problem:
`https://mooreamood.com` doesn't work

### Check DNS:

1. **Go to your DNS provider** (Cloudflare/Porkbun)
2. **Verify records**:
   - CNAME: `@` → Vercel's CNAME value
   - CNAME: `www` → Vercel's CNAME value
3. **Wait for DNS propagation** (5-30 minutes)

### Check Vercel:

1. **Vercel Dashboard** → Your project → Settings → Domains
2. **Domain status**:
   - ✅ "Valid Configuration" = Good
   - ⚠️ "Pending" = Wait for DNS
   - ❌ "Invalid" = Check DNS records

---

## 🚨 Quick Diagnostic Steps

### Step 1: Check Railway Service

```bash
# Replace with your Railway URL
curl https://your-railway-url.railway.app/health
```

**Expected:** `{"status":"healthy",...}`
**If error:** Service not running or not public

### Step 2: Check Railway Status

1. Railway Dashboard → Your service
2. Status should be "Active"
3. If "Crashed", check logs

### Step 3: Check Railway Logs

1. Railway → Your service → "Logs" tab
2. Look for:
   - ✅ "Database tables created"
   - ✅ "Services initialized successfully"
   - ❌ Any error messages

### Step 4: Check Deployment

1. Railway → Deployments tab
2. Latest should be "Active" (green)
3. If failed, click it and check logs

---

## 📋 Checklist

Before reporting issues, verify:

- [ ] Railway service is **public** (Settings → Networking)
- [ ] Service status is **"Active"** (not Crashed)
- [ ] Latest deployment is **successful** (green checkmark)
- [ ] Using correct Railway URL (ends in `.railway.app`)
- [ ] Testing with `https://` (not `http://`)
- [ ] Waiting for deployment to finish (if still building)
- [ ] Checked Railway logs for errors

---

## 🎯 Most Likely Issues

Based on your recent crashes:

1. **Service not exposed** → Make it public in Railway Settings
2. **Service still crashing** → Check logs for the latest error
3. **Deployment failed** → Check Build/Deploy logs for errors

---

## 💡 Quick Fix

**If Railway service is not accessible:**

1. Railway Dashboard → Your service
2. Settings → Networking
3. Click "Generate Domain" or toggle "Public"
4. Copy the URL
5. Test: Visit `https://your-url.railway.app/health`

**This should work immediately!** ✅

