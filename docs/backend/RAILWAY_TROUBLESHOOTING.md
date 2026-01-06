# Railway Deployment Troubleshooting

## Common Issues and Fixes

### Issue: Build Timeout / Large Packages

**Problem:** Torch and torchvision are very large (several GB) and can cause Railway build timeouts.

**Solutions:**

1. **Use CPU-only torch** (already configured in requirements.txt)
   - Smaller download size
   - Faster installation
   - Still works for ML features

2. **If still failing, try installing in stages:**

Update `nixpacks.toml`:
```toml
[phases.install]
cmds = [
  "pip install --upgrade pip setuptools wheel",
  "pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv pydantic pydantic-settings",
  "pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cpu",
  "pip install transformers pillow git+https://github.com/openai/CLIP.git",
  "pip install -r requirements.txt --no-cache-dir"
]
```

3. **For waitlist-only deployment (no ML):**
   - Use `requirements-minimal.txt` instead
   - Update Railway build command to: `pip install -r requirements-minimal.txt`

### Issue: Python Version

**Problem:** Wrong Python version specified.

**Solution:** Already fixed - using Python 3.11 in `nixpacks.toml`

### Issue: Missing Git

**Problem:** CLIP package requires git to install.

**Solution:** Already added `git` to nixpacks.toml

### Issue: Services Fail to Start

**Problem:** ML services fail but app should still work for waitlist.

**Solution:** Already fixed - services initialize with try/except, app starts even if ML fails.

### Issue: Environment Variables

**Problem:** Missing DATABASE_URL or other required vars.

**Solution:** Make sure all environment variables are set in Railway:
- `DATABASE_URL` (required)
- `SECRET_KEY` (required)
- `ALLOWED_ORIGINS` (optional, for CORS)
- API keys (optional)

### Issue: Port Binding

**Problem:** App doesn't bind to Railway's PORT.

**Solution:** Already configured - uses `$PORT` environment variable.

### Check Railway Logs

1. Go to Railway dashboard
2. Click on your service
3. Go to "Deployments" tab
4. Click on latest deployment
5. View "Logs" to see exact error

### Quick Test Commands

After deployment, test:
```bash
curl https://your-app.up.railway.app/health
curl -X POST https://your-app.up.railway.app/api/v1/waitlist/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"Test"}'
```

### If All Else Fails

1. Check Railway logs for specific error
2. Try minimal requirements (waitlist only)
3. Consider splitting into two services:
   - API service (waitlist, auth)
   - ML service (moodboard generation)

