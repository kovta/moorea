# 🔗 Railway GitHub Integration Guide

## How Railway Works with GitHub

Railway can automatically deploy your app whenever you push to GitHub. Here's how to check and configure it.

---

## ✅ Check if Railway is Connected to GitHub

### Step 1: Check Railway Dashboard

1. **Go to Railway Dashboard**: https://railway.app
2. **Click on your project** (e.g., "moorea")
3. **Click on your service** (e.g., "moorea" backend service)
4. **Go to "Settings" tab**
5. **Look for "Source" section**

**What you should see:**
- ✅ **Connected to GitHub**: Shows your repository name (e.g., `kovta/moorea`)
- ✅ **Branch**: Shows which branch it's watching (usually `main` or `master`)
- ✅ **Auto Deploy**: Should be **enabled** (green toggle)

---

## 🔧 How to Connect Railway to GitHub (If Not Connected)

### Option 1: Connect During Service Creation

1. **In Railway Dashboard** → Click "New Project"
2. **Select "Deploy from GitHub repo"**
3. **Authorize Railway** to access your GitHub account
4. **Select your repository**: `kovta/moorea`
5. **Select branch**: `main`
6. **Set Root Directory**: `backend` (important!)
7. **Click "Deploy"**

### Option 2: Connect Existing Service

1. **Go to your service** → "Settings" tab
2. **Find "Source" section**
3. **Click "Connect GitHub"** or "Change Source"
4. **Select your repository** and branch
5. **Set Root Directory**: `backend`
6. **Enable "Auto Deploy"** toggle
7. **Save**

---

## 🚀 How Auto-Deploy Works

### When Railway Deploys Automatically:

✅ **Every push to the connected branch** (usually `main`)
- When you run: `git push origin main`
- Railway detects the push
- Automatically starts a new deployment
- Builds and deploys your app

✅ **Pull Requests** (if configured)
- Some Railway plans support PR previews
- Creates a temporary deployment for testing

### When Railway Does NOT Deploy:

❌ **Pushes to other branches** (unless configured)
❌ **Local commits** (only pushes to GitHub trigger deployments)
❌ **If "Auto Deploy" is disabled**

---

## 🔍 Verify Auto-Deploy is Working

### Test It:

1. **Make a small change** to your code (e.g., add a comment)
2. **Commit and push**:
   ```bash
   git add .
   git commit -m "Test auto-deploy"
   git push origin main
   ```
3. **Go to Railway Dashboard** → Your service → "Deployments" tab
4. **You should see**:
   - New deployment starting within 30-60 seconds
   - Status: "Building" → "Deploying" → "Active"
   - Commit message shows your latest commit

---

## ⚙️ Railway Settings to Check

### 1. Root Directory

**Critical Setting!** Make sure it's set to `backend`:

1. **Service Settings** → "Source" section
2. **Root Directory**: Should be `backend`
3. **Why?** Your code is in the `backend/` folder, not the repo root

### 2. Branch

- **Default Branch**: Usually `main` or `master`
- **Change it**: If you want to deploy from a different branch

### 3. Auto Deploy Toggle

- **Should be ON** (green/enabled)
- **If OFF**: Railway won't auto-deploy on pushes

---

## 🐛 Troubleshooting

### Problem: Railway Not Deploying on Push

**Check:**
1. ✅ Is "Auto Deploy" enabled in Railway settings?
2. ✅ Is the correct branch selected?
3. ✅ Is Root Directory set to `backend`?
4. ✅ Did you push to the correct branch?
5. ✅ Check Railway → Deployments tab for any errors

**Fix:**
- Go to Railway → Service → Settings → Source
- Verify all settings are correct
- Try manually triggering a deployment: "Deployments" → "Redeploy"

### Problem: Railway Deploying Wrong Code

**Check:**
- Root Directory is set to `backend` (not empty or `/`)
- Branch is set to `main` (or your production branch)

### Problem: Build Fails After Push

**Check:**
- Railway → Deployments → Click on failed deployment → "Build Logs"
- Look for error messages
- Common issues:
  - Missing dependencies in `requirements.txt`
  - Wrong Python version
  - Missing environment variables

---

## 📊 Monitor Deployments

### View Deployment History:

1. **Railway Dashboard** → Your service
2. **"Deployments" tab**
3. **See all deployments** with:
   - Commit hash
   - Commit message
   - Status (Active, Failed, Building)
   - Timestamp

### View Deployment Logs:

1. **Click on a deployment**
2. **"Build Logs"** - See what happened during build
3. **"Deploy Logs"** - See what happened during deployment/runtime

---

## 🎯 Quick Checklist

Before pushing code, verify:

- [ ] Railway is connected to your GitHub repo
- [ ] Auto Deploy is enabled
- [ ] Root Directory is set to `backend`
- [ ] Branch is set to `main` (or your production branch)
- [ ] You're pushing to the correct branch

---

## 💡 Pro Tips

1. **Test Locally First**: Always test changes locally before pushing
2. **Check Logs**: After pushing, check Railway logs to ensure deployment succeeded
3. **Use Branches**: Consider using feature branches, then merge to `main` for production
4. **Monitor Deployments**: Watch the first deployment after a push to catch errors early

---

## ✅ Current Status

Based on your recent pushes, Railway **should** be connected and auto-deploying. 

**To verify:**
1. Go to Railway → Your service → Settings → Source
2. Check if it shows your GitHub repo
3. Check if "Auto Deploy" is enabled
4. Look at "Deployments" tab - you should see recent deployments matching your git commits

**If you see deployments matching your recent commits** → ✅ Railway is connected and working!

**If you don't see recent deployments** → Follow the setup steps above to connect Railway to GitHub.

