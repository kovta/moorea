# 🔧 Fix Vercel 404 Error

## Problem
Visiting `https://mooreamood.com` shows:
```
404: NOT_FOUND
Code: NOT_FOUND
```

This means:
- ✅ DNS is working (domain resolves to Vercel)
- ❌ Vercel can't find a deployment for this domain

---

## 🔍 Step 1: Check if Project is Deployed

### In Vercel Dashboard:

1. **Go to Vercel**: https://vercel.com
2. **Check your projects list**
3. **Do you see a project for your frontend?**
   - If **NO** → You need to deploy (see Step 2)
   - If **YES** → Check Step 3

---

## 🚀 Step 2: Deploy Your Frontend (If Not Deployed)

### Option A: Deploy from GitHub (Recommended)

1. **In Vercel Dashboard**:
   - Click **"Add New..."** → **"Project"**
   - **Import Git Repository** → Select your GitHub repo
   - Click **"Import"**

2. **Configure Project Settings**:
   - **Framework Preset**: `Create React App` (or `React`)
   - **Root Directory**: `frontend` ⚠️ **IMPORTANT!**
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
   - **Install Command**: `npm install` (or leave default)

3. **Add Environment Variables**:
   - Click **"Environment Variables"**
   - Add:
     - **Name**: `REACT_APP_API_URL`
     - **Value**: Your Railway backend URL (e.g., `https://moorea-production.up.railway.app`)
   - Click **"Add"**

4. **Deploy**:
   - Click **"Deploy"**
   - Wait 2-5 minutes for build to complete

### Option B: Deploy via Vercel CLI

```bash
cd /Users/kovacstamaspal/dev/moorea/frontend
npm install -g vercel
vercel
# Follow the prompts
```

---

## 🔗 Step 3: Assign Domain to Project

### If Project Exists But Domain Not Connected:

1. **In Vercel Dashboard**:
   - Go to your **project** (not the domain settings)
   - Click **"Settings"** tab
   - Click **"Domains"** in the left sidebar

2. **Add Your Domain**:
   - In the "Domains" section, you should see:
     - `mooreamood.com` (if already added)
     - `www.mooreamood.com` (if already added)
   
3. **If Domains Are Missing**:
   - Click **"Add Domain"**
   - Enter: `mooreamood.com`
   - Click **"Add"**
   - Repeat for `www.mooreamood.com`

4. **Verify Domain Assignment**:
   - Both domains should show:
     - ✅ **"Valid Configuration"**
     - **Production** environment selected
     - Connected to your project

---

## ⚙️ Step 4: Check Project Configuration

### Verify Root Directory:

1. **Vercel Dashboard** → Your project → **"Settings"** → **"General"**
2. **Check "Root Directory"**:
   - Should be: `frontend`
   - If it's blank or wrong, click **"Edit"** and set it to `frontend`

### Verify Build Settings:

1. **Vercel Dashboard** → Your project → **"Settings"** → **"General"**
2. **Check "Build & Development Settings"**:
   - **Framework Preset**: `Create React App` or `React`
   - **Build Command**: `npm run build` (or leave default)
   - **Output Directory**: `build` (or leave default)
   - **Install Command**: `npm install` (or leave default)

---

## 📋 Step 5: Check Deployment Status

1. **Vercel Dashboard** → Your project → **"Deployments"** tab
2. **Look at the latest deployment**:
   - ✅ **Green checkmark** = Success
   - ❌ **Red X** = Failed (check logs)
   - 🔄 **Spinning** = Still deploying

### If Deployment Failed:

1. **Click on the failed deployment**
2. **Check "Build Logs"**:
   - Look for error messages
   - Common issues:
     - Missing dependencies
     - TypeScript errors
     - Build command errors
3. **Fix the error** and push to GitHub (Vercel will auto-redeploy)

---

## 🧪 Step 6: Test Vercel URL

Before testing the custom domain, test the Vercel URL:

1. **Vercel Dashboard** → Your project
2. **Look for the deployment URL** (e.g., `https://mooreamood-abc123.vercel.app`)
3. **Visit that URL** in your browser
4. **Does it work?**
   - ✅ **Yes** → Domain assignment issue (see Step 3)
   - ❌ **No** → Deployment issue (see Step 5)

---

## 🔄 Step 7: Force Redeploy

If everything looks correct but still 404:

1. **Vercel Dashboard** → Your project → **"Deployments"**
2. **Click the "..." menu** on the latest deployment
3. **Click "Redeploy"**
4. **Wait 2-5 minutes**

---

## ✅ Success Checklist

After following these steps, you should have:

- [ ] Project deployed in Vercel
- [ ] Domain `mooreamood.com` assigned to project
- [ ] Domain `www.mooreamood.com` assigned to project
- [ ] Both domains show "Valid Configuration"
- [ ] Latest deployment shows ✅ (green checkmark)
- [ ] Root directory set to `frontend`
- [ ] `REACT_APP_API_URL` environment variable set
- [ ] Vercel URL works (e.g., `https://mooreamood-abc123.vercel.app`)
- [ ] Custom domain works (`https://mooreamood.com`)

---

## 🆘 Still Not Working?

### Check These:

1. **Is the domain assigned to the right project?**
   - Vercel → Domains → Check which project each domain is connected to

2. **Is there a `vercel.json` file?**
   - If yes, check if it has routing rules that might conflict

3. **Are there multiple Vercel projects?**
   - Make sure you're looking at the correct project

4. **Check Vercel logs:**
   - Project → Deployments → Click on deployment → "View Function Logs"

### Contact Support:

If still not working after checking all above:
- Vercel Support: https://vercel.com/support
- Include: Project name, domain, deployment logs

