# Pinterest API Compliance - Action Plan

**Date**: January 2025  
**Status**: 🚨 **CRITICAL FIXES REQUIRED BEFORE APPLICATION**

---

## 🎯 Priority Order

### **PHASE 1: CRITICAL DATA STORAGE FIXES** (Must Complete First)
These are blockers that will cause immediate rejection.

### **PHASE 2: REQUIRED DOCUMENTATION** (Before Application)
These are required for a complete application.

### **PHASE 3: BEST PRACTICES** (Can Complete After Application)
These improve compliance but aren't blockers.

---

## 📋 PHASE 1: CRITICAL DATA STORAGE FIXES

### ✅ Task 1.1: Remove Pinterest from Cache Service
**Priority**: 🔴 CRITICAL  
**Status**: ❌ Not Started  
**Estimated Time**: 15 minutes

**Problem**: 
- `services/cache_service.py` documentation mentions caching Pinterest data
- Even if Pinterest client doesn't use cache, the documentation suggests it might

**Required Changes**:
1. Update `services/cache_service.py`:
   - Remove "Pinterest" from cache documentation
   - Add explicit note: "Pinterest data is NEVER cached"
   - Update TTL documentation to exclude Pinterest

**Files to Modify**:
- `backend/services/cache_service.py` (lines 15, 157)

**Code Changes**:
```python
# Change from:
# - API Response Cache: 1 hour (search results from Unsplash, Pexels, Flickr, Pinterest)

# To:
# - API Response Cache: 1 hour (search results from Unsplash, Pexels, Flickr)
# - Pinterest Compliance: Pinterest data is NEVER cached - always fetched fresh
```

---

### ✅ Task 1.2: Filter Pinterest Images from Saved Moodboards
**Priority**: 🔴 CRITICAL  
**Status**: ❌ Not Started  
**Estimated Time**: 30 minutes

**Problem**: 
- When users save moodboards, Pinterest images are saved to database
- This violates Pinterest's "no storage" policy
- `app/routes/moodboard_save.py` accepts all images without filtering

**Required Changes**:
1. Update `app/routes/moodboard_save.py`:
   - Filter out Pinterest images before saving
   - Add validation to reject Pinterest images
   - Add logging when Pinterest images are filtered

**Files to Modify**:
- `backend/app/routes/moodboard_save.py`

**Code Changes**:
```python
@router.post("/", response_model=MoodboardResponse)
async def create_moodboard(
    moodboard_data: MoodboardCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new moodboard for the current user."""
    
    # Filter out Pinterest images to comply with "no storage" policy
    filtered_images = [
        img for img in moodboard_data.images 
        if img.get('source_api', '').lower() != 'pinterest'
    ]
    
    pinterest_count = len(moodboard_data.images) - len(filtered_images)
    if pinterest_count > 0:
        logger.info(f"Filtered out {pinterest_count} Pinterest images from saved moodboard (compliance)")
    
    db_moodboard = Moodboard(
        title=moodboard_data.title,
        description=moodboard_data.description,
        aesthetic=moodboard_data.aesthetic,
        images=filtered_images,  # Use filtered images
        user_id=current_user.id
    )
    # ... rest of code
```

**Frontend Changes**:
- Update `frontend/src/components/SaveMoodboard.tsx` to filter Pinterest images before sending
- Show user notification: "Pinterest images cannot be saved (compliance requirement)"

---

### ✅ Task 1.3: Verify Pinterest Client Doesn't Use Cache
**Priority**: 🟡 MEDIUM  
**Status**: ✅ Already Verified (Pinterest client doesn't use cache)  
**Estimated Time**: 5 minutes (verification only)

**Verification**:
- ✅ `services/pinterest_client.py` does NOT call `cache_service`
- ✅ Pinterest client makes direct API calls
- ✅ No caching logic in Pinterest client

**Action**: Add explicit comment in Pinterest client confirming no cache usage

---

### ✅ Task 1.4: Add Rate Limiting for Pinterest API
**Priority**: 🟡 MEDIUM  
**Status**: ❌ Not Started  
**Estimated Time**: 1 hour

**Problem**: 
- No rate limiting implemented
- Could hit Pinterest rate limits and get blocked

**Required Changes**:
1. Create rate limiter for Pinterest API calls
2. Track calls per user/IP
3. Implement exponential backoff on rate limit errors

**Files to Create/Modify**:
- `backend/services/rate_limiter.py` (new)
- `backend/services/pinterest_client.py` (add rate limiting)

**Implementation**:
```python
# Simple in-memory rate limiter (Redis optional)
class PinterestRateLimiter:
    def __init__(self):
        self.calls_per_minute = 100  # Pinterest limit
        self.calls = {}  # {user_id: [timestamps]}
    
    async def check_rate_limit(self, user_id: str) -> bool:
        # Check if user exceeded rate limit
        # Return True if allowed, False if rate limited
        pass
```

---

## 📋 PHASE 2: REQUIRED DOCUMENTATION

### ✅ Task 2.1: Create Terms of Service Page
**Priority**: 🟡 MEDIUM  
**Status**: ❌ Not Started  
**Estimated Time**: 1 hour

**Required Changes**:
1. Create `frontend/src/pages/TermsOfService.tsx`
2. Add route in `frontend/src/App.tsx`
3. Link in footer/navigation
4. Include Pinterest API usage terms

**Files to Create**:
- `frontend/src/pages/TermsOfService.tsx`

**Files to Modify**:
- `frontend/src/App.tsx` (add route)
- `frontend/src/components/Footer.tsx` (if exists, add link)

**Content Requirements**:
- Service description
- User responsibilities
- Pinterest API usage terms
- Data handling policies
- Limitation of liability

---

### ✅ Task 2.2: Document Rate Limiting Implementation
**Priority**: 🟢 LOW  
**Status**: ❌ Not Started  
**Estimated Time**: 30 minutes

**Required Changes**:
1. Document rate limiting in README or API docs
2. Add comments in code explaining rate limits
3. Log rate limit events

**Files to Modify**:
- `backend/services/pinterest_client.py` (add documentation)
- `README.md` or create `API_DOCUMENTATION.md`

---

### ✅ Task 2.3: Document API Usage Flow
**Priority**: 🟢 LOW  
**Status**: ❌ Not Started  
**Estimated Time**: 45 minutes

**Required Changes**:
1. Create documentation explaining:
   - Which Pinterest endpoints are used
   - How data flows through the system
   - How compliance is maintained
   - No-storage policy implementation

**Files to Create**:
- `PINTEREST_API_USAGE.md`

---

## 📋 PHASE 3: BEST PRACTICES (Post-Application)

### ✅ Task 3.1: Add Comprehensive Error Handling
**Priority**: 🟢 LOW  
**Status**: ❌ Not Started

**Improvements**:
- Better error messages for Pinterest API failures
- Graceful degradation when Pinterest unavailable
- User-friendly error messages

---

### ✅ Task 3.2: Add API Usage Metrics
**Priority**: 🟢 LOW  
**Status**: ❌ Not Started

**Improvements**:
- Track Pinterest API call counts
- Monitor rate limit usage
- Log compliance events

---

## ✅ Implementation Checklist

### Phase 1: Critical Fixes
- [ ] **1.1** Remove Pinterest from cache documentation
- [ ] **1.2** Filter Pinterest images from saved moodboards (backend)
- [ ] **1.2** Filter Pinterest images from saved moodboards (frontend)
- [ ] **1.3** Add comment confirming no cache in Pinterest client
- [ ] **1.4** Implement rate limiting for Pinterest API

### Phase 2: Documentation
- [ ] **2.1** Create Terms of Service page
- [ ] **2.1** Add Terms of Service route
- [ ] **2.1** Link Terms of Service in footer
- [ ] **2.2** Document rate limiting
- [ ] **2.3** Create API usage documentation

### Phase 3: Best Practices
- [ ] **3.1** Add comprehensive error handling
- [ ] **3.2** Add API usage metrics

---

## 🚀 Quick Start Guide

### To Fix Critical Issues (30-45 minutes):

1. **Remove Pinterest from cache docs** (5 min)
   ```bash
   # Edit backend/services/cache_service.py
   # Remove "Pinterest" from line 15
   ```

2. **Filter Pinterest from saved moodboards** (30 min)
   ```bash
   # Edit backend/app/routes/moodboard_save.py
   # Add filtering logic in create_moodboard()
   ```

3. **Add rate limiting** (1 hour)
   ```bash
   # Create backend/services/rate_limiter.py
   # Update backend/services/pinterest_client.py
   ```

4. **Create Terms of Service** (1 hour)
   ```bash
   # Create frontend/src/pages/TermsOfService.tsx
   # Add route in frontend/src/App.tsx
   ```

**Total Time**: ~2.5 hours for critical fixes

---

## 📝 Notes

### Why These Fixes Are Critical:

1. **Data Storage Violation**: Pinterest explicitly prohibits storing any Pinterest data. Saving Pinterest images in moodboards is a direct violation.

2. **Cache Documentation**: Even if Pinterest isn't cached, mentioning it in cache docs suggests it might be, which could cause rejection.

3. **Terms of Service**: Required for API applications - shows you have proper legal documentation.

4. **Rate Limiting**: Prevents hitting Pinterest rate limits and getting blocked.

### What's Already Good:

- ✅ Pinterest client doesn't use cache (verified)
- ✅ Pinterest images link back to Pinterest (just fixed)
- ✅ Privacy policy updated with "no storage" language (just fixed)
- ✅ No Pinterest branding in UI (already done)

---

## 🎯 Next Steps

1. **Start with Task 1.2** (filter Pinterest from saved moodboards) - this is the biggest blocker
2. **Then Task 1.1** (remove from cache docs) - quick fix
3. **Then Task 2.1** (Terms of Service) - required for application
4. **Then Task 1.4** (rate limiting) - prevents issues

Would you like me to start implementing these fixes?

