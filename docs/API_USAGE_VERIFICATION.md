# 🔍 Verifying Unsplash and Pexels API Usage

## ✅ Yes, Both APIs Are Integrated!

Both **Unsplash** and **Pexels** APIs are actively used in the moodboard generation pipeline.

## 📋 How They're Used

### 1. **Integration Points**

Both APIs are called in `backend/services/moodboard_service.py` in the `_fetch_candidates` method:

```python
# For each keyword (top 3 keywords are used):
- Unsplash: Called first if UNSPLASH_ACCESS_KEY is configured
- Pexels: Called as fallback if PEXELS_API_KEY is configured
- Pinterest: Called if user consented (optional)
```

### 2. **API Call Flow**

1. **Keyword Selection**: Top 3 keywords from aesthetic classification
2. **Concurrent API Calls**: Both Unsplash and Pexels are called **simultaneously** for each keyword
3. **Image Collection**: Results from both APIs are combined
4. **Deduplication**: Duplicate URLs are removed
5. **Similarity Ranking**: CLIP model ranks images by similarity to uploaded image

### 3. **Configuration**

API keys are read from environment variables:
- `UNSPLASH_ACCESS_KEY` → Unsplash API
- `PEXELS_API_KEY` → Pexels API

These should be set in **Railway → Your Service → Variables**

## 🔍 How to Verify They're Working

### Method 1: Check Railway Logs

When you upload an image, look for these log messages:

```
🔍 Fetching images for keywords: ['keyword1', 'keyword2', 'keyword3']
   Images per keyword: X
   Unsplash API key configured: True/False
   Pexels API key configured: True/False
   Pinterest consent: True/False
⚡ SPEED MODE: Fetching from 2 API(s) for 3 keywords (6 total requests)
✅ API call 1 succeeded: X images
✅ API call 2 succeeded: X images
...
📊 API Results: X succeeded, Y failed, Z total images fetched
⚡ Fast fetch: X unique candidates (target: 20)
```

**What to look for:**
- ✅ `Unsplash API key configured: True` → Unsplash is available
- ✅ `Pexels API key configured: True` → Pexels is available
- ✅ `Fetching from 2 API(s)` → Both APIs are being used
- ✅ `API call X succeeded: Y images` → Shows successful API calls
- ❌ `⚠️ Unsplash API key not configured` → Unsplash key missing
- ❌ `⚠️ Pexels API key not configured` → Pexels key missing

### Method 2: Check Image Sources

In the moodboard result, each image has a `source_api` field:
- `"unsplash"` → Image came from Unsplash
- `"pexels"` → Image came from Pexels
- `"pinterest"` → Image came from Pinterest (if consented)

### Method 3: Check API Client Logs

Look for specific API client logs:

**Unsplash:**
```
Unsplash: Found X images for 'keyword'
```

**Pexels:**
```
Pexels: Found X images for 'keyword'
```

### Method 4: Check for Errors

Look for these error patterns:

**If API keys are missing:**
```
⚠️ Unsplash API key not configured, skipping Unsplash for 'keyword'
⚠️ Pexels API key not configured, skipping Pexels for 'keyword'
❌ No API keys configured! Cannot fetch images.
```

**If API calls fail:**
```
❌ API call X failed: HTTPError: ...
❌ API call X failed: TimeoutError: ...
```

**If no images are found:**
```
❌ No image candidates found! Check API keys and network connectivity.
```

## 🛠️ Troubleshooting

### Issue: "Unsplash API key not configured"

**Solution:**
1. Go to Railway → Your Service → Variables
2. Add `UNSPLASH_ACCESS_KEY` with your Unsplash access key
3. Redeploy the service

### Issue: "Pexels API key not configured"

**Solution:**
1. Go to Railway → Your Service → Variables
2. Add `PEXELS_API_KEY` with your Pexels API key
3. Redeploy the service

### Issue: "No image candidates found"

**Possible causes:**
1. Both API keys are missing
2. API calls are timing out (5 second timeout)
3. Network connectivity issues
4. API rate limits exceeded

**Check logs for:**
- `❌ API call X failed` messages
- `⚠️ API calls timed out after 5 seconds`
- HTTP error codes (401, 403, 429, etc.)

### Issue: Only one API is working

**Check:**
- Both API keys are set in Railway
- Both show `True` in the logs
- Look for `Fetching from 2 API(s)` message

## 📊 Expected Behavior

### When Both APIs Are Configured:

1. **For each keyword** (top 3 keywords):
   - Unsplash API call
   - Pexels API call
   - Total: **6 API calls** (3 keywords × 2 APIs)

2. **Images per keyword**: ~2-7 images (depends on `max_candidates` setting)

3. **Total images fetched**: ~12-20 images (before deduplication)

4. **After similarity ranking**: Top 12 images selected for moodboard

### When Only One API Is Configured:

- Only that API is used
- Fewer images available
- Still should work, but with less variety

## 🎯 Quick Verification Checklist

- [ ] Check Railway logs for `Unsplash API key configured: True`
- [ ] Check Railway logs for `Pexels API key configured: True`
- [ ] Look for `Fetching from 2 API(s)` message
- [ ] Verify `✅ API call X succeeded` messages appear
- [ ] Check that `📊 API Results` shows images fetched
- [ ] Verify moodboard shows images (not just uploaded image)

## 💡 Pro Tips

1. **Check logs immediately after upload**: The API calls happen during moodboard generation
2. **Look for the keyword logs**: Shows which keywords triggered the searches
3. **Check success/failure counts**: `X succeeded, Y failed` tells you if APIs are working
4. **Monitor timeout warnings**: If you see `⚠️ API calls timed out`, the timeout might be too short

## 📝 Code References

- **Unsplash Client**: `backend/services/unsplash_client.py`
- **Pexels Client**: `backend/services/pexels_client.py`
- **Moodboard Service**: `backend/services/moodboard_service.py` (lines 308-398)
- **Settings**: `backend/config/settings.py` (lines 36-37)

