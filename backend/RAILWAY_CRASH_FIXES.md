# Railway Deployment Crash Fixes

## Why Your App Keeps Crashing After Running

Based on the error logs and code analysis, here are the main reasons your Railway deployment fails after running for a while:

### 1. **Database Connection Exhaustion** ✅ FIXED
**Problem:** No connection pooling configured, leading to connection exhaustion over time.

**Symptoms:**
- App works initially, then crashes after some time
- Database connection errors in logs
- "Too many connections" errors

**Fix Applied:**
- Added connection pooling (`pool_size=5`, `max_overflow=10`)
- Added `pool_pre_ping=True` to verify connections before use
- Added `pool_recycle=3600` to refresh stale connections
- Added connection timeouts

### 2. **FastAPI/Pydantic Version Mismatch** ✅ FIXED
**Problem:** FastAPI 0.104.1 not fully compatible with Pydantic v2.

**Symptoms:**
- `AttributeError: 'FieldInfo' object has no attribute 'in_'`
- App crashes immediately on startup

**Fix Applied:**
- Upgraded FastAPI to `>=0.109.0` (Pydantic v2 compatible)
- Updated uvicorn and python-multipart

### 3. **Memory Issues (ML Models)** ⚠️ MONITOR
**Problem:** CLIP models loaded into memory can consume 500MB-2GB RAM.

**Symptoms:**
- App crashes with OOM (Out of Memory) errors
- Railway restarts the service repeatedly
- Slow performance

**Current Status:**
- ML services initialize with try/except (graceful degradation)
- If ML fails, app still runs for waitlist functionality
- Consider disabling ML features if memory is tight

**Recommendations:**
- Monitor Railway memory usage in dashboard
- If crashes persist, consider lazy-loading models (load on first use)
- Or disable ML features entirely for waitlist-only deployment

### 4. **Missing Redis Connection** ✅ HANDLED
**Problem:** Redis not configured in Railway, but cache service tries to connect.

**Current Status:**
- Cache service gracefully handles Redis failures
- App continues without caching if Redis unavailable
- No crash - just degraded performance

### 5. **No Health Check Verification** ✅ IMPROVED
**Problem:** Health check didn't verify actual database connectivity.

**Fix Applied:**
- Health check now verifies database connection
- Returns "degraded" status if database check fails
- Helps Railway detect real issues

### 6. **Stale Database Connections** ✅ FIXED
**Problem:** Long-running connections can become stale and fail.

**Fix Applied:**
- `pool_recycle=3600` refreshes connections after 1 hour
- `pool_pre_ping=True` verifies connections before use

## Monitoring Your Deployment

### Check Railway Logs:
1. Go to Railway dashboard → Your service → Logs
2. Look for:
   - Memory usage warnings
   - Database connection errors
   - ML model loading errors
   - Health check failures

### Key Metrics to Watch:
- **Memory Usage**: Should stay under Railway's limit (check your plan)
- **Database Connections**: Should stay within pool limits (5-15 connections)
- **Restart Frequency**: Frequent restarts indicate a problem

## If Crashes Continue

### Option 1: Disable ML Features (Waitlist Only)
If you only need the waitlist functionality:

1. Set environment variable in Railway:
   ```
   DISABLE_ML=1
   ```

2. Update `app/main.py` to skip ML initialization if this is set.

### Option 2: Increase Railway Resources
- Upgrade to a plan with more memory
- Railway free tier has limited resources

### Option 3: Use Lazy Loading
Load ML models only when needed (first request), not at startup.

## Environment Variables Checklist

Make sure these are set in Railway:

✅ **Required:**
- `DATABASE_URL` - Your Supabase connection string
- `SECRET_KEY` - For JWT tokens

✅ **Optional but Recommended:**
- `ALLOWED_ORIGINS` - Your frontend URL (e.g., `https://mooreamood.com`)
- `REDIS_URL` - If using Redis caching

✅ **Optional:**
- API keys (Unsplash, Pexels, etc.) - Only needed for ML features

## Next Steps

1. **Deploy the fixes** - The connection pooling fix should help significantly
2. **Monitor for 24 hours** - Watch Railway logs and metrics
3. **Check memory usage** - If still crashing, likely memory issue
4. **Consider disabling ML** - If only using waitlist, disable ML features

## Testing Locally

Before deploying, test the connection pooling fix:

```bash
cd backend
python -c "from database import engine; print('✅ Database engine created with pooling')"
```

The app should now be more stable! 🚀

