# 🗺️ Frontend Routing Guide

## Current Routing Structure

### Routes Defined in `App.tsx`:

| Path | Component | Purpose | Status |
|------|-----------|---------|--------|
| `/` | `LandingPage` | Pre-launch waitlist signup | ✅ Exists |
| `/app` | `Home` | Main moodboard creation app | ✅ Exists |
| `/saved` | `SavedMoodboards` | View saved moodboards | ✅ Exists |

---

## Current Behavior

### Local Development (`npm start`):
- `http://localhost:3000/` → Shows **LandingPage** (waitlist signup)
- `http://localhost:3000/app` → Shows **Home** (moodboard creation)
- `http://localhost:3000/saved` → Shows **SavedMoodboards**

### Deployed (Vercel):
- `https://mooreamood.com/` → Shows **LandingPage** (waitlist signup)
- `https://mooreamood.com/app` → Shows **Home** (moodboard creation)
- `https://mooreamood.com/saved` → Shows **SavedMoodboards**

**Note:** Currently, both local and deployed show the same content at the same paths.

---

## Understanding Your Requirements

You mentioned:
> "the local frontend is the join the waitlist site, and the deployed one is the create a moodboard site"

### Option 1: Environment-Based Routing (Recommended for Pre-Launch)

**For Pre-Launch:**
- Deployed: Show landing page at `/` (waitlist)
- Local: Show landing page at `/` (for testing waitlist)

**For Post-Launch:**
- Deployed: Show main app at `/` (moodboard creation)
- Landing page: Move to `/waitlist` or remove

### Option 2: Different Behavior Now

If you want different behavior **right now**:
- Local: Landing page at `/`
- Deployed: Main app at `/`

This would require environment-based routing.

---

## Recommended Setup (Pre-Launch Strategy)

### Current Setup (Pre-Launch):
```
/              → LandingPage (waitlist)     [Both local & deployed]
/app           → Home (moodboard creation)  [Both local & deployed]
/saved         → SavedMoodboards            [Both local & deployed]
```

### Post-Launch Setup (Future):
```
/              → Home (moodboard creation)  [Main app]
/waitlist      → LandingPage (optional)      [If keeping waitlist]
/app           → Home (redirect to /)        [Or remove]
/saved         → SavedMoodboards
```

---

## Missing Routes Check

### ✅ All Required Routes Exist:
- [x] Landing page route (`/`)
- [x] Main app route (`/app`)
- [x] Saved moodboards route (`/saved`)

### Additional Routes to Consider:

1. **Privacy Policy** (`/privacy`)
   - Referenced in `LandingPage.tsx` footer
   - Currently missing

2. **Terms of Service** (`/terms`)
   - Common for production sites
   - Currently missing

3. **About** (`/about`)
   - Optional informational page
   - Currently missing

---

## Next Steps

1. **Decide on routing strategy:**
   - Keep current (same for local & deployed)?
   - Or implement environment-based routing?

2. **Create missing pages:**
   - Privacy Policy page
   - Terms of Service page (optional)

3. **Plan for post-launch:**
   - How to switch from landing page to main app at `/`?

