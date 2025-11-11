# 🧪 Test Waitlist Endpoint

## Quick Test

Replace `YOUR_RAILWAY_URL` with your actual Railway URL:

```bash
curl -X POST https://YOUR_RAILWAY_URL.railway.app/api/v1/waitlist/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"Test User"}'
```

**Expected response:**
```json
{
  "success": true,
  "message": "Successfully added to waitlist! We'll notify you when we launch.",
  "email": "test@example.com"
}
```

**If you get 405:**
- Check if the route is registered
- Check if the service is running
- Check Railway logs

