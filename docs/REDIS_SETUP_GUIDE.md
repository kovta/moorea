# How to Check and Run Redis

## Quick Status Check

### Option 1: Check if redis-cli is available
```powershell
redis-cli ping
```
If you see `PONG` → Redis is running ✅
If you see command not found → Redis not installed

---

## How to Get Redis Running

### Option A: Docker (Easiest if Docker is running)
```powershell
# Start Redis container
docker run -d -p 6379:6379 --name moorea-redis redis:latest

# Verify it's running
docker ps | findstr moorea-redis

# Check Redis is working
docker exec moorea-redis redis-cli ping
# Should return: PONG
```

### Option B: Windows Subsystem for Linux (WSL)
```powershell
# If you have WSL2 installed:
wsl -d <distro-name> redis-server

# In another terminal, verify:
wsl -d <distro-name> redis-cli ping
```

### Option C: Install Redis on Windows via Chocolatey
```powershell
# If you have Chocolatey installed:
choco install redis

# Then start it:
redis-server

# In another terminal, verify:
redis-cli ping
```

### Option D: Use Python redis module without Redis
If you can't run Redis, I can modify the code to use an in-memory store instead.

---

## What's Actually Needed?

Redis is used for:
- Storing OAuth state for CSRF protection
- Caching access tokens
- Managing token expiration

If you can't run Redis right now, we have alternatives:

1. **Use Redis Cloud** (free tier): https://app.redislabs.com/
   - Get connection string
   - Update `.env` with `REDIS_URL=redis://...`

2. **Modify the code** to use an in-memory dictionary (development only)

3. **Start Docker Desktop** - easiest solution

---

## Quick Fix: Start Docker Desktop

1. Open **Docker Desktop** application (search in Start menu)
2. Wait for it to fully initialize (~30 seconds)
3. Then run:
   ```powershell
   docker run -d -p 6379:6379 --name moorea-redis redis:latest
   ```

---

## Once Redis is Running

You'll see this when you test:
```powershell
$ docker exec moorea-redis redis-cli ping
PONG  ← This means it's working!
```

Then you can start the backend:
```powershell
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

---

**Need help starting Docker or want to skip Redis?** Let me know!
