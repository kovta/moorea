# 🚀 Deployment Guide: Go Live with Your Landing Page

This guide will walk you through deploying your backend to Railway and frontend to Vercel.

---

## 📋 Prerequisites Checklist

- [x] ✅ Supabase database connected and working
- [x] ✅ Backend running locally and tested
- [x] ✅ Frontend running locally and tested
- [x] ✅ Custom domain purchased (you mentioned you bought one)
- [ ] GitHub repository set up (recommended for easy deployment)

---

## 🎯 Step 1: Prepare Your Code

### 1.1 Commit Your Code to Git

```bash
cd /Users/kovacstamaspal/dev/moorea
git add .
git commit -m "Add landing page with Supabase waitlist integration"
git push origin main
```

**Note:** Make sure `.env` files are in `.gitignore` (they should NOT be committed!)

---

## 🔧 Step 2: Deploy Backend to Railway

### 2.1 Create Railway Account

1. Go to https://railway.app
2. Sign up with GitHub (easiest)
3. Click "New Project"

### 2.2 Connect Your Repository

1. Select "Deploy from GitHub repo"
2. Choose your `moorea` repository
3. Select the `backend` folder as the root directory

### 2.3 Configure Environment Variables

In Railway dashboard, go to your service → **Variables** tab, add:

```bash
# Database
DATABASE_URL=postgresql://postgres.djezqevhrdygxkhskflw:[YOUR-PASSWORD]@aws-1-eu-north-1.pooler.supabase.com:6543/postgres

# External APIs (add your actual keys)
UNSPLASH_ACCESS_KEY=your_unsplash_key
PEXELS_API_KEY=your_pexels_key
FLICKR_API_KEY=your_flickr_key

# Security (generate a random secret)
SECRET_KEY=your-super-secret-key-change-this-to-random-string

# Optional: Redis (if you want to use it)
REDIS_URL=redis://localhost:6379
```

**Important:** 
- Copy your exact `DATABASE_URL` from your local `.env` file
- Generate a secure `SECRET_KEY` (you can use: `openssl rand -hex 32`)

### 2.4 Railway Will Auto-Detect

Railway should automatically detect:
- ✅ Python project
- ✅ `requirements.txt`
- ✅ `nixpacks.toml` or `railway.json`
- ✅ Start command from `railway.json`

### 2.5 Get Your Backend URL

Once deployed, Railway will give you a URL like:
```
https://your-app-name.up.railway.app
```

**Save this URL** - you'll need it for the frontend!

### 2.6 Test Your Backend

```bash
curl https://your-backend-url.up.railway.app/health
```

Should return: `{"status":"healthy",...}`

---

## 🌐 Step 3: Deploy Frontend to Vercel

### 3.1 Create Vercel Account

1. Go to https://vercel.com
2. Sign up with GitHub
3. Click "Add New Project"

### 3.2 Import Your Repository

1. Select your `moorea` repository
2. Set **Root Directory** to: `frontend`
3. Framework Preset: **React**
4. Build Settings:
   - Build Command: `npm run build`
   - Output Directory: `build`
   - Install Command: `npm install`

### 3.3 Configure Environment Variables

In Vercel project settings → **Environment Variables**, add:

```bash
REACT_APP_API_URL=https://your-backend-url.up.railway.app/api/v1
```

Replace `your-backend-url.up.railway.app` with your actual Railway backend URL.

### 3.4 Deploy

Click "Deploy" - Vercel will:
1. Install dependencies
2. Build your React app
3. Deploy to a `.vercel.app` domain

### 3.5 Get Your Frontend URL

Vercel will give you a URL like:
```
https://your-app-name.vercel.app
```

---

## 🔗 Step 4: Connect Custom Domain

### 4.1 Configure Domain in Vercel

1. Go to your Vercel project → **Settings** → **Domains**
2. Add your custom domain (e.g., `moorea.com`)
3. Vercel will show DNS records to add

### 4.2 Update DNS Records

Go to your domain registrar (where you bought the domain) and add:

**For root domain (moorea.com):**
- Type: `A`
- Name: `@`
- Value: `76.76.21.21` (Vercel's IP)

**For www (www.moorea.com):**
- Type: `CNAME`
- Name: `www`
- Value: `cname.vercel-dns.com`

**Or use Vercel's recommended DNS records** (they'll show you exactly what to add)

### 4.3 Wait for DNS Propagation

DNS changes can take 5 minutes to 48 hours (usually < 1 hour).

### 4.4 Verify Domain

Vercel will automatically verify your domain once DNS propagates.

---

## 🔄 Step 5: Update Frontend API URL

After connecting your domain, update the frontend environment variable:

1. Go to Vercel → Your Project → **Settings** → **Environment Variables**
2. Update `REACT_APP_API_URL`:
   ```
   REACT_APP_API_URL=https://your-backend-url.up.railway.app/api/v1
   ```
3. Redeploy (or wait for auto-deploy)

---

## 🎨 Step 6: Update CORS in Backend

Update your backend CORS to allow your custom domain:

1. Go to Railway → Your Service → **Variables**
2. Add a new variable:
   ```
   ALLOWED_ORIGINS=https://moorea.com,https://www.moorea.com,https://your-app-name.vercel.app
   ```

3. Update `app/main.py` to use this:

```python
# CORS middleware
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then commit and push - Railway will auto-deploy.

---

## ✅ Step 7: Final Testing

### 7.1 Test Landing Page

1. Visit your custom domain: `https://moorea.com`
2. Try signing up with a test email
3. Check Supabase dashboard → `waitlist_users` table to verify

### 7.2 Test API Endpoints

```bash
# Health check
curl https://your-backend-url.up.railway.app/health

# Waitlist signup
curl -X POST https://your-backend-url.up.railway.app/api/v1/waitlist/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"Test"}'
```

### 7.3 Verify Database

Check Supabase dashboard → Table Editor → `waitlist_users` to see signups.

---

## 🎯 Quick Reference

### Backend (Railway)
- **Dashboard:** https://railway.app
- **URL:** `https://your-app-name.up.railway.app`
- **Logs:** Railway dashboard → Deployments → View logs

### Frontend (Vercel)
- **Dashboard:** https://vercel.com
- **URL:** `https://your-app-name.vercel.app`
- **Custom Domain:** `https://moorea.com` (after DNS setup)

### Database (Supabase)
- **Dashboard:** https://supabase.com/dashboard
- **Connection:** Already configured ✅

---

## 🐛 Troubleshooting

### Backend not responding
- Check Railway logs for errors
- Verify `DATABASE_URL` is correct
- Check if tables are created (they auto-create on first start)

### Frontend can't reach backend
- Verify `REACT_APP_API_URL` is set correctly
- Check CORS settings in backend
- Test backend URL directly: `curl https://your-backend-url.up.railway.app/health`

### Domain not working
- Check DNS records are correct
- Wait for DNS propagation (can take up to 48 hours)
- Use `dig moorea.com` or `nslookup moorea.com` to check DNS

### Database connection issues
- Verify `DATABASE_URL` in Railway matches your Supabase connection string
- Check Supabase dashboard for any issues
- Ensure you're using the **pooled connection string** (Transaction mode)

---

## 📊 Monitoring

### Railway
- View logs: Dashboard → Deployments → Logs
- Monitor usage: Dashboard → Metrics
- Set up alerts: Dashboard → Settings → Notifications

### Vercel
- View analytics: Dashboard → Analytics
- View logs: Dashboard → Deployments → Logs
- Monitor performance: Dashboard → Speed Insights

### Supabase
- View data: Dashboard → Table Editor
- Monitor usage: Dashboard → Settings → Usage
- View logs: Dashboard → Logs

---

## 🎉 You're Live!

Once everything is set up:
- ✅ Your landing page is live at `https://moorea.com`
- ✅ Waitlist signups are saved to Supabase
- ✅ Backend API is accessible
- ✅ Everything is connected and working

**Next Steps:**
- Share your landing page!
- Monitor signups in Supabase
- Collect emails for your launch
- When ready, build out the full app features

---

## 💰 Cost Estimate

### Free Tier (for getting started):
- **Railway:** $5/month (includes $5 credit - free for first month)
- **Vercel:** Free (Hobby plan)
- **Supabase:** Free (generous free tier)
- **Domain:** ~$10-15/year

**Total: ~$5/month** (after Railway free credit expires)

### Scaling Up:
- Railway: Pay-as-you-go (scales with usage)
- Vercel: Free tier is generous, upgrade if needed
- Supabase: Free tier is very generous

---

## 🆘 Need Help?

- **Railway Docs:** https://docs.railway.app
- **Vercel Docs:** https://vercel.com/docs
- **Supabase Docs:** https://supabase.com/docs

Good luck with your launch! 🚀
