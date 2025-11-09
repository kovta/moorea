# 🚀 Deploy Waitlist to Production

## ✅ Good News!

The waitlist frontend is **already part of your React app** and will automatically be deployed to `/waitlist` when you deploy to Vercel. You just need to ensure it's connected to your production backend.

---

## 📋 Current Setup

### Frontend (Already Done ✅):
- ✅ Waitlist form component exists (`WaitlistForm.tsx`)
- ✅ Landing page exists (`LandingPage.tsx`)
- ✅ Route configured: `/waitlist` → `LandingPage`
- ✅ API function: `subscribeToWaitlist()` calls `/api/v1/waitlist/subscribe`

### Backend (Already Done ✅):
- ✅ Waitlist endpoint: `POST /api/v1/waitlist/subscribe`
- ✅ Connected to Supabase production database
- ✅ Creates entries in `waitlist_users` table

---

## 🔧 What You Need to Do

### Step 1: Get Your Railway Backend URL

1. **Go to Railway Dashboard**: https://railway.app
2. **Click on your backend service**
3. **Go to "Settings" → "Networking"**
4. **Copy your public URL** (e.g., `https://moorea-production.up.railway.app`)

---

### Step 2: Set Environment Variable in Vercel

The frontend needs to know where your production backend is:

1. **Go to Vercel Dashboard**: https://vercel.com
2. **Click on your project** (the one with `mooreamood.com`)
3. **Go to "Settings" → "Environment Variables"**
4. **Add/Update this variable**:

   **Name:** `REACT_APP_API_URL`
   
   **Value:** Your Railway backend URL (e.g., `https://moorea-production.up.railway.app`)
   
   **Environment:** Production (and Preview if you want)

5. **Click "Save"**

---

### Step 3: Verify CORS is Configured

Make sure your Railway backend allows requests from your Vercel domain:

1. **Go to Railway** → Your service → "Variables" tab
2. **Check `ALLOWED_ORIGINS` is set**:
   ```
   https://mooreamood.com,https://www.mooreamood.com
   ```
3. **If not set, add it** (Railway will auto-redeploy)

---

### Step 4: Redeploy Frontend

After setting the environment variable:

1. **Vercel Dashboard** → Your project → "Deployments"
2. **Click "..." menu** on latest deployment
3. **Click "Redeploy"**
4. **Wait 2-5 minutes** for deployment to complete

**OR** just push a new commit to trigger auto-deploy:
```bash
git commit --allow-empty -m "Trigger Vercel redeploy"
git push
```

---

## ✅ Verification

### Test the Waitlist:

1. **Visit**: `https://mooreamood.com/waitlist`
2. **Fill out the form**:
   - Enter email: `test@example.com`
   - Enter name (optional)
   - Click "Join the Waitlist"
3. **Check for success message**: "Successfully added to waitlist!"
4. **Verify in Supabase**:
   - Go to Supabase Dashboard
   - Table Editor → `waitlist_users` table
   - You should see the new entry

### Check Browser Console:

1. **Open browser console** (F12)
2. **Look for**:
   ```
   🔧 Environment check: {
     REACT_APP_API_URL: "https://moorea-production.up.railway.app",
     API_BASE: "https://moorea-production.up.railway.app",
     NODE_ENV: "production"
   }
   ```
3. **If you see errors**, check:
   - Is `REACT_APP_API_URL` set correctly?
   - Is CORS configured in Railway?
   - Is Railway backend running?

---

## 🔍 Troubleshooting

### Issue: "Network Error" or CORS Error

**Solution:**
1. Check `ALLOWED_ORIGINS` in Railway includes your domain
2. Check Railway backend is running (visit `/health` endpoint)
3. Check `REACT_APP_API_URL` is set correctly in Vercel

### Issue: "Failed to add email to waitlist"

**Solution:**
1. Check Railway logs for database errors
2. Verify `DATABASE_URL` is set in Railway
3. Check Supabase connection is working

### Issue: Form submits but no success message

**Solution:**
1. Check browser console for errors
2. Check Network tab to see API response
3. Verify backend endpoint is accessible

---

## 📊 How It Works

```
User visits: https://mooreamood.com/waitlist
    ↓
Frontend (Vercel) loads LandingPage component
    ↓
User fills form and clicks "Join Waitlist"
    ↓
Frontend calls: REACT_APP_API_URL + /api/v1/waitlist/subscribe
    ↓
Backend (Railway) receives request
    ↓
Backend saves to Supabase database (waitlist_users table)
    ↓
Backend returns success response
    ↓
Frontend shows success message
```

---

## ✅ Success Checklist

- [ ] Railway backend is running and accessible
- [ ] `REACT_APP_API_URL` is set in Vercel environment variables
- [ ] `ALLOWED_ORIGINS` includes your domain in Railway
- [ ] Frontend is deployed to Vercel
- [ ] Can visit `https://mooreamood.com/waitlist`
- [ ] Form submission works
- [ ] Email appears in Supabase `waitlist_users` table

---

## 🎯 Summary

**The waitlist is already deployed!** It's part of your React app at `/waitlist`. You just need to:

1. ✅ Set `REACT_APP_API_URL` in Vercel → Points to Railway backend
2. ✅ Ensure CORS is configured in Railway → Allows requests from your domain
3. ✅ Redeploy frontend → Applies the environment variable

That's it! The waitlist will automatically connect to your production database through the Railway backend.

