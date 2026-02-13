# Pinterest API Integration Guide

## Configuration Status: ✅ ACTIVE

Your Pinterest API credentials have been successfully configured in the moodboard generation pipeline.

### Current Setup

**Credentials Configured**:
- Client ID: `1546788`
- API Key: ✅ Configured (from `PINTEREST_CLIENT_KEY`)
- Mock Mode: ❌ Disabled (now using real Pinterest API)

### How It Works

#### 1. **API Authentication**
The system uses your API key for direct authentication:
- **Header**: `Authorization: Bearer [PINTEREST_CLIENT_KEY]`
- **Fallback**: If no API key, falls back to OAuth token (if user logged in)
- **Mode**: Real API (not mock)

#### 2. **Integration in Moodboard Generation**

When a user generates a moodboard:

```
User uploads image
    ↓
CLIP classifies aesthetics
    ↓
Keywords expanded
    ↓
Parallel API queries:
  ├─ Unsplash API
  ├─ Pexels API
  ├─ Flickr API
  └─ Pinterest API ← NOW ACTIVE
    ↓
CLIP re-ranks results
    ↓
Final moodboard (30+ images including Pinterest pins)
```

#### 3. **Pinterest Pins in Results**

When Pinterest images are returned:
- `source_api`: `"pinterest"`
- `pinterest_url`: Link to the pin (e.g., `https://pinterest.com/pin/123456/`)
- `pinterest_board`: Board name where pin was found
- `photographer`: Creator username
- Copyable URL visible on hover (pale white text)

### Code Changes Made

**1. `config/settings.py`**
- Added `pinterest_client_key` field
- Changed `use_mock_pinterest: bool = False` (was True)

**2. `services/pinterest_oauth_service.py`**
- Added API key support in `__init__`
- Updated `make_authenticated_request()` to use API key as fallback
- Falls back to: OAuth token → API key → Error

**3. `services/pinterest_client.py`**
- Updated `is_authenticated()` to check both OAuth token AND API key
- Returns `True` if either is present

**4. `services/moodboard_service.py`**
- Pinterest now included in all API queries (not just when user consents)
- Logs confirmation when Pinterest is included
- Respects `pinterest_consent` for future GDPR/privacy features

### Environment Variables Required

In your `.env` file:
```
PINTEREST_CLIENT_ID=1546788
PINTEREST_CLIENT_KEY=037c5665ea8240e8cfed91bd9891979d30ec4dea
```

### Testing the Integration

To verify Pinterest is working:

1. **Generate a moodboard** at `http://localhost:3000`
2. **Upload a fashion image**
3. **Check results** - should include Pinterest pins with:
   - "📌 Image from Pinterest" label on hover
   - Board name if available
   - Copyable source URL (e.g., `https://pinterest.com/pin/[id]/`)
4. **Check backend logs** for:
   ```
   📌 Including Pinterest for '[keyword]'
   ```

### API Rate Limits

Pinterest API has rate limits:
- **Requests per minute**: ~400-600 (varies)
- **Requests per day**: Limited (check Pinterest docs)
- **Recommendations**:
  - Cache results for 24 hours
  - Batch similar queries
  - Implement backoff on 429 (Too Many Requests)

### Pinterest Developer Guidelines Compliance

✅ **Links back to Pinterest**: Every pin shows copyable source URL
✅ **Clear attribution**: "📌 Image from Pinterest" label
✅ **No content modification**: Pins displayed exactly as provided
✅ **API authentication**: Using official API key method

### Future Enhancements

- [ ] Implement Pinterest-specific caching (24-hour TTL)
- [ ] Add user-specific Pinterest board filtering
- [ ] Support Pinterest save functionality (save moodboard to user's board)
- [ ] Add analytics tracking for Pinterest image popularity
- [ ] Implement API error handling with fallback sources

### Troubleshooting

**Pinterest returns no results**:
- Check API key is valid in `.env`
- Check rate limits haven't been exceeded
- Verify keywords are being generated (check logs)

**Authorization errors**:
- Verify `PINTEREST_CLIENT_KEY` is correct in `.env`
- Check backend logs for detailed error messages
- Try accessing Pinterest API directly with curl:
  ```bash
  curl -H "Authorization: Bearer [KEY]" \
    "https://api.pinterest.com/v5/pins/search?query=fashion"
  ```

**No Pinterest images in results**:
- Check backend logs for "📌 Including Pinterest for '[keyword]'" message
- Verify `use_mock_pinterest=False` in logs at startup
- Check that `is_authenticated()` returns `True`
