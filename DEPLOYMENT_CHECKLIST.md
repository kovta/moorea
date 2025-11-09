# ✅ Deployment Checklist

Use this checklist to track your deployment progress.

## 📋 Pre-Deployment

- [ ] Code committed to Git
- [ ] `.env` files are in `.gitignore` (NOT committed)
- [ ] Backend tested locally
- [ ] Frontend tested locally
- [ ] Database connection verified
- [ ] Waitlist signup tested

## 🚂 Railway (Backend)

- [ ] Railway account created
- [ ] GitHub repository connected
- [ ] Backend service deployed
- [ ] Environment variables added:
  - [ ] `DATABASE_URL`
  - [ ] `UNSPLASH_ACCESS_KEY`
  - [ ] `PEXELS_API_KEY`
  - [ ] `FLICKR_API_KEY`
  - [ ] `SECRET_KEY` (generated)
- [ ] Backend URL saved: `https://________________.up.railway.app`
- [ ] Health check working: `curl https://your-backend-url/health`

## ⚡ Vercel (Frontend)

- [ ] Vercel account created
- [ ] GitHub repository connected
- [ ] Frontend service deployed
- [ ] Environment variable added:
  - [ ] `REACT_APP_API_URL` = `https://your-backend-url.up.railway.app/api/v1`
- [ ] Frontend URL saved: `https://________________.vercel.app`
- [ ] Landing page loads correctly

## 🌐 Custom Domain

- [ ] Domain purchased
- [ ] DNS records added:
  - [ ] A record for root domain
  - [ ] CNAME record for www
- [ ] Domain verified in Vercel
- [ ] SSL certificate active (automatic)
- [ ] Custom domain working: `https://________________`

## 🔧 Configuration

- [ ] Backend CORS updated with production domains
- [ ] Frontend API URL updated
- [ ] All services redeployed after config changes

## ✅ Testing

- [ ] Landing page loads at custom domain
- [ ] Waitlist signup form works
- [ ] Signups appear in Supabase database
- [ ] Backend API responds correctly
- [ ] No console errors in browser
- [ ] Mobile responsive (test on phone)

## 📊 Monitoring Setup

- [ ] Railway logs accessible
- [ ] Vercel analytics enabled
- [ ] Supabase dashboard accessible
- [ ] Email notifications configured (optional)

## 🎉 Launch

- [ ] Everything tested and working
- [ ] Ready to share with users!
- [ ] Monitor signups in Supabase

---

## 🔗 Quick Links

**Save these URLs:**
- Backend: `________________________________`
- Frontend: `________________________________`
- Custom Domain: `________________________________`
- Supabase Dashboard: `https://supabase.com/dashboard`

---

## 📝 Notes

_Use this space to jot down any issues or important information during deployment:_


