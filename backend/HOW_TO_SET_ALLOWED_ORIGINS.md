# 🔧 How to Set ALLOWED_ORIGINS in Railway

## Step-by-Step Instructions

### Step 1: Go to Railway Dashboard

1. Open your browser
2. Go to: https://railway.app
3. Log in to your account
4. Click on your project (e.g., "moorea" or "spectacular-mercy")

### Step 2: Open Your Service

1. Click on your backend service (usually named "moorea")
2. You should see tabs: **Deployments**, **Variables**, **Metrics**, **Settings**

### Step 3: Go to Variables Tab

1. Click on the **"Variables"** tab
2. You'll see a list of existing environment variables (if any)
3. Look for a button that says **"New Variable"** or **"Add Variable"** or **"+"**

### Step 4: Add ALLOWED_ORIGINS

1. Click **"New Variable"** (or the "+" button)
2. A form will appear with two fields:
   - **Variable Name** (or "Key")
   - **Value**

3. Fill in the form:
   - **Variable Name:** Type exactly: `ALLOWED_ORIGINS`
   - **Value:** Type your frontend URLs, separated by commas (no spaces after commas):
     ```
     https://mooreamood.com,https://www.mooreamood.com
     ```
   
   **If you don't have a custom domain yet**, use your Vercel URL:
   ```
   https://your-app-name.vercel.app
   ```

4. Click **"Add"** or **"Save"**

### Step 5: Wait for Redeploy

- Railway will automatically detect the new variable
- It will automatically trigger a new deployment
- Wait 2-3 minutes for the deployment to complete

### Step 6: Verify It's Set

1. Go to Railway → Your service → **"Logs"** tab
2. Look for this line (should appear after redeploy):
   ```
   CORS configured for production origins: ['https://mooreamood.com', 'https://www.mooreamood.com']
   ```
   
   **If you see this** → ✅ Success! CORS is configured correctly.
   
   **If you still see the warning** → The variable might not be set correctly. Check:
   - Variable name is exactly `ALLOWED_ORIGINS` (case-sensitive)
   - No extra spaces
   - URLs include `https://`

---

## 📋 Example Values

### If you have a custom domain:
```
https://mooreamood.com,https://www.mooreamood.com
```

### If using Vercel (no custom domain yet):
```
https://moorea.vercel.app
```

### If testing locally too:
```
https://mooreamood.com,https://www.mooreamood.com,http://localhost:3000
```

---

## ⚠️ Important Notes

1. **No spaces after commas** - Wrong: `https://example.com, https://www.example.com`
2. **Include https://** - Don't forget the protocol
3. **No trailing slashes** - Wrong: `https://example.com/`
4. **Case-sensitive** - Variable name must be exactly `ALLOWED_ORIGINS`

---

## 🎯 Quick Checklist

- [ ] Opened Railway Dashboard
- [ ] Clicked on your service
- [ ] Went to "Variables" tab
- [ ] Clicked "New Variable"
- [ ] Set name: `ALLOWED_ORIGINS`
- [ ] Set value: Your frontend URL(s)
- [ ] Clicked "Add"/"Save"
- [ ] Waited for redeploy
- [ ] Checked logs for "CORS configured for production origins"

---

## 🐛 Troubleshooting

### Variable not showing up?
- Make sure you clicked "Add" or "Save"
- Refresh the page
- Check if Railway is still deploying

### Still seeing the warning?
- Double-check the variable name (exact spelling, case-sensitive)
- Make sure URLs are correct (include https://)
- Wait for deployment to finish
- Check Railway logs after deployment completes

### Can't find "Variables" tab?
- Make sure you're in the service view (not project view)
- Look for "Environment" or "Env" tab (some Railway versions use different names)

---

## ✅ Success!

Once you see this in the logs:
```
CORS configured for production origins: ['https://mooreamood.com', 'https://www.mooreamood.com']
```

You're all set! Your frontend can now communicate with your backend. 🎉


