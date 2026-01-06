# 🔒 reCAPTCHA Setup Guide

## Overview

reCAPTCHA has been integrated into the login and registration forms to protect against bots and spam.

## ✅ What's Been Implemented

### Frontend:
- ✅ reCAPTCHA component added to `LoginForm.tsx`
- ✅ reCAPTCHA component added to `RegisterForm.tsx`
- ✅ Form validation requires reCAPTCHA completion
- ✅ reCAPTCHA resets on error or success

### Backend:
- ✅ reCAPTCHA verification service (`recaptcha_service.py`)
- ✅ Token verification in login endpoint
- ✅ Token verification in register endpoint
- ✅ Graceful fallback if reCAPTCHA is not configured

## 🔑 Required Environment Variables

### Frontend (Vercel):
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add:
   - **Key**: `REACT_APP_RECAPTCHA_SITE_KEY`
   - **Value**: Your reCAPTCHA Site Key (from Google)
   - **Environment**: Production (and Preview if needed)

### Backend (Railway):
1. Go to Railway Dashboard → Your Service → Variables
2. Add:
   - **Key**: `RECAPTCHA_SECRET_KEY`
   - **Value**: Your reCAPTCHA Secret Key (from Google)

## 📝 Getting reCAPTCHA Keys

1. **Go to Google reCAPTCHA Admin Console**:
   - Visit: https://www.google.com/recaptcha/admin/create

2. **Create a new site**:
   - **Label**: Moorea Moodboard (or your choice)
   - **reCAPTCHA type**: Select "reCAPTCHA v2" → "I'm not a robot" Checkbox
   - **Domains**: 
     - Add your production domain: `mooreamood.com`
     - Add your Vercel domain: `your-app.vercel.app`
     - For local development: `localhost` (optional)
   - **Accept the reCAPTCHA Terms of Service**
   - Click **Submit**

3. **Copy your keys**:
   - **Site Key**: Use this for `REACT_APP_RECAPTCHA_SITE_KEY` (frontend)
   - **Secret Key**: Use this for `RECAPTCHA_SECRET_KEY` (backend)

## 🚀 Deployment Steps

### 1. Set Frontend Environment Variable (Vercel):
```bash
# In Vercel Dashboard:
REACT_APP_RECAPTCHA_SITE_KEY=your_site_key_here
```

### 2. Set Backend Environment Variable (Railway):
```bash
# In Railway Dashboard:
RECAPTCHA_SECRET_KEY=your_secret_key_here
```

### 3. Redeploy:
- **Vercel**: Will auto-deploy when you push changes, or trigger manual redeploy
- **Railway**: Will auto-deploy when you push changes, or trigger manual redeploy

## 🧪 Testing

### Local Development:
1. Add `REACT_APP_RECAPTCHA_SITE_KEY` to your `.env` file in `frontend/`:
   ```
   REACT_APP_RECAPTCHA_SITE_KEY=your_site_key_here
   ```

2. Add `RECAPTCHA_SECRET_KEY` to your `.env` file in `backend/`:
   ```
   RECAPTCHA_SECRET_KEY=your_secret_key_here
   ```

3. Restart your development servers

### Production Testing:
1. Go to your website
2. Click "Sign In / Sign Up"
3. You should see the reCAPTCHA checkbox
4. Complete the reCAPTCHA
5. Try to login/register - it should work

## ⚠️ Important Notes

1. **Graceful Degradation**: 
   - If reCAPTCHA keys are not configured, the forms will still work (for development)
   - In production, make sure both keys are set

2. **Domain Configuration**:
   - Make sure your reCAPTCHA site includes all domains where your app is hosted
   - For Vercel: Include both `your-app.vercel.app` and your custom domain

3. **Security**:
   - **Never commit** your Secret Key to git
   - **Never expose** your Secret Key in frontend code
   - Site Key is safe to use in frontend (it's public)

## 🔍 Troubleshooting

### reCAPTCHA not showing:
- Check that `REACT_APP_RECAPTCHA_SITE_KEY` is set in Vercel
- Check browser console for errors
- Verify the domain is added to your reCAPTCHA site configuration

### "reCAPTCHA verification failed":
- Check that `RECAPTCHA_SECRET_KEY` is set in Railway
- Verify the Secret Key matches the Site Key (they're a pair)
- Check Railway logs for reCAPTCHA verification errors
- Make sure the domain matches what's configured in Google reCAPTCHA

### "reCAPTCHA verification required" but no checkbox:
- This means backend expects reCAPTCHA but frontend isn't sending it
- Check that `REACT_APP_RECAPTCHA_SITE_KEY` is set
- Check that the reCAPTCHA component is rendering (inspect the form)

## 📚 Additional Resources

- [Google reCAPTCHA Documentation](https://developers.google.com/recaptcha/docs/display)
- [react-google-recaptcha Documentation](https://www.npmjs.com/package/react-google-recaptcha)

