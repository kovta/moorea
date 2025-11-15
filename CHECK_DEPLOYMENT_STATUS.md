# 🔍 How to Check if Railway and Vercel Have Redeployed

## 🚂 Railway (Backend)

### Method 1: Check Deployment Status in Dashboard

1. **Go to Railway Dashboard**: https://railway.app
2. **Click on your service** (e.g., `moorea-production` or `serene-grace`)
3. **Go to "Deployments" tab**
4. **Look at the latest deployment**:
   - ✅ **Green checkmark** = Successfully deployed
   - ❌ **Red X** = Failed deployment
   - 🔄 **Spinning icon** = Currently deploying
   - ⏸️ **Paused** = Deployment paused

5. **Check the commit info**:
   - Click on the latest deployment
   - Look at the commit message (should match your latest commit)
   - Look at the commit SHA (first 7 characters should match your git commit)
   - **Example**: If you pushed commit `d17ee2e`, you should see `d17ee2e` in the deployment

### Method 2: Check Deployment Logs

1. **Railway Dashboard** → Your service → **"Deployments" tab**
2. **Click on the latest deployment**
3. **Check "Build Logs"**:
   - Should show successful build
   - Look for: `✅ Build completed successfully`
   - Should NOT show errors

4. **Check "Deploy Logs"**:
   - Should show service starting
   - Look for: `Application startup complete`
   - Should NOT show crash errors

### Method 3: Check Real-Time Logs

1. **Railway Dashboard** → Your service → **"Logs" tab**
2. **Look for recent log entries** with timestamps
3. **If you see your new log messages**, the deployment is live:
   - Look for: `🔄 Re-ranking X candidates using CLIP similarity`
   - Look for: `📊 Similarity scores - Min: X, Max: X`
   - These are from the latest code changes

### Method 4: Check via API

```bash
# Replace with your Railway URL
curl https://moorea-production.up.railway.app/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "timestamp": "...",
  "version": "1.0.0"
}
```

If you get a response, the service is running (but may not be the latest code).

---

## ▲ Vercel (Frontend)

### Method 1: Check Deployment Status in Dashboard

1. **Go to Vercel Dashboard**: https://vercel.com
2. **Click on your project** (e.g., `moorea` or `moorea-frontend`)
3. **Look at the "Deployments" section**:
   - ✅ **Green "Ready"** = Successfully deployed
   - ❌ **Red "Error"** = Failed deployment
   - 🔄 **"Building"** = Currently deploying
   - ⏸️ **"Queued"** = Waiting to deploy

4. **Check the commit info**:
   - Hover over or click on the latest deployment
   - Look at the commit message (should match your latest commit)
   - Look at the commit SHA (should match your git commit)
   - **Example**: If you pushed commit `d17ee2e`, you should see it in Vercel

### Method 2: Check Deployment Logs

1. **Vercel Dashboard** → Your project → **Click on latest deployment**
2. **Check "Build Logs"**:
   - Should show: `✓ Build completed`
   - Should NOT show errors
   - Look for: `Creating an optimized production build...`

3. **Check "Runtime Logs"** (if available):
   - Should show successful deployment
   - Should NOT show runtime errors

### Method 3: Check Build Output

1. **Vercel Dashboard** → Your project → **Latest deployment**
2. **Click "View Function Logs"** or **"View Build Logs"**
3. **Look for**:
   - `✓ Compiled successfully`
   - `✓ Linting and checking validity of types`
   - `✓ Collecting page data`
   - `✓ Generating static pages`

### Method 4: Check via Browser

1. **Visit your site**: https://mooreamood.com
2. **Open browser DevTools** (F12 or Cmd+Option+I)
3. **Go to "Network" tab**
4. **Refresh the page**
5. **Check the response headers**:
   - Look for `x-vercel-deployment-url` header
   - This shows which deployment is being served

### Method 5: Check Build Time

1. **Vercel Dashboard** → Your project
2. **Look at the latest deployment timestamp**
3. **Compare with your git push time**:
   - If deployment time is **after** your push → ✅ Latest code
   - If deployment time is **before** your push → ⚠️ Old code

---

## 🎯 Quick Verification Checklist

### Railway:
- [ ] Latest deployment shows ✅ (green checkmark)
- [ ] Commit SHA matches your latest git commit
- [ ] Build logs show successful build
- [ ] Deploy logs show service started
- [ ] Real-time logs show new log messages (if you added logging)

### Vercel:
- [ ] Latest deployment shows ✅ "Ready" (green)
- [ ] Commit SHA matches your latest git commit
- [ ] Build logs show successful build
- [ ] Site loads without errors
- [ ] New features/changes are visible (if you made UI changes)

---

## ⏱️ Typical Deployment Times

- **Railway**: 2-5 minutes after git push
- **Vercel**: 1-3 minutes after git push

**If it's been longer than 5 minutes**, check:
1. Did the deployment fail? (Check logs)
2. Is auto-deploy enabled? (Check settings)
3. Did you push to the correct branch? (Should be `main`)

---

## 🚨 If Deployment Shows Old Code

### Railway:
1. **Check "Deployments" tab** - Is there a newer deployment queued?
2. **Manually trigger redeploy**:
   - Railway → Your service → Settings → Source
   - Click "Redeploy" or disconnect/reconnect GitHub
3. **Check if auto-deploy is enabled**:
   - Railway → Your service → Settings → Source
   - Ensure "Auto Deploy" is ON

### Vercel:
1. **Check "Deployments" tab** - Is there a newer deployment queued?
2. **Manually trigger redeploy**:
   - Vercel → Your project → Deployments
   - Click "..." menu on latest deployment
   - Click "Redeploy"
3. **Check if auto-deploy is enabled**:
   - Vercel → Your project → Settings → Git
   - Ensure "Production Branch" is set to `main`
   - Ensure "Auto Deploy" is enabled

---

## 💡 Pro Tips

1. **Use commit messages**: Make descriptive commit messages so you can easily identify which deployment matches which code
2. **Check immediately after push**: Both platforms usually start deploying within 30 seconds
3. **Watch the logs**: Real-time logs show exactly when new code is running
4. **Use git tags**: Tag important releases to track which version is deployed

---

## 🔍 For Your Current Situation

**To verify the latest moodboard service changes are deployed:**

1. **Railway**:
   - Go to Railway → Your service → Deployments
   - Check if latest deployment shows commit `d17ee2e` (or your latest commit)
   - Check Logs tab for: `🔄 Re-ranking X candidates` (new log message)

2. **Vercel**:
   - Go to Vercel → Your project → Deployments
   - Check if latest deployment shows your latest commit
   - Visit https://mooreamood.com and test the moodboard feature

**If you see the new log messages in Railway**, the backend is updated! ✅

