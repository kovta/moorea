# Pinterest API Compliance Issues - Pre-Approval Checklist

**Date**: January 2025  
**Status**: ⚠️ **CRITICAL ISSUES IDENTIFIED**

---

## 🚨 Critical Issues (Must Fix Before Application)

### 1. **Data Storage Violation** - HIGHEST PRIORITY
**Issue**: Storing Pinterest data violates Pinterest's core policy: *"You may not store any information accessed through any Pinterest Materials, including the API."*

**Current Violations**:
- ✅ **Cache Service** (`services/cache_service.py`): Caches Pinterest URLs and metadata with 1-hour TTL
- ✅ **Database Storage**: When users save moodboards, Pinterest URLs are stored in database
- ✅ **Moodboard Results**: Pinterest pin URLs, board names, and metadata are stored in response objects

**Pinterest Policy**:
> "Except for campaign analytics information accessed about your account, you may not store any information accessed through any Pinterest Materials, including the API. Instead, call the API each time you need to access information."

**Required Fixes**:
1. **Remove Pinterest from cache entirely** - No caching of Pinterest data, even with TTL
2. **Don't store Pinterest URLs in database** - When saving moodboards, exclude Pinterest images or only store a flag that Pinterest was used
3. **Call API each time** - Always fetch Pinterest content fresh, never from cache or database

**Code Changes Needed**:
- `services/cache_service.py`: Exclude Pinterest data from all caches
- `services/moodboard_service.py`: Don't cache Pinterest API responses
- Database models: Don't persist Pinterest URLs/metadata
- `app/routes/moodboard_save.py`: Filter out Pinterest data before saving

---

### 2. **Missing User Consent Mechanism** - HIGH PRIORITY
**Issue**: Removed Pinterest consent checkbox, but Pinterest requires explicit user consent.

**Current State**:
- ❌ No UI for Pinterest consent
- ❌ `pinterestConsent` always defaults to `false`
- ❌ Users cannot opt-in to Pinterest content

**Pinterest Requirement**:
- Users must explicitly consent to Pinterest data usage
- Consent must be clear and informed
- Users should understand what Pinterest data is used for

**Required Fixes**:
1. **Restore consent UI** - But make it generic (don't mention "Pinterest" by name)
2. **Alternative**: Use generic "Include additional image sources" checkbox
3. **Privacy Policy Link**: Link to privacy policy explaining Pinterest usage

**Suggested Implementation**:
```typescript
// Generic consent checkbox (no Pinterest branding)
<label>
  <input type="checkbox" />
  Include images from additional sources to enhance your moodboard
</label>
<p className="text-xs text-gray-500">
  <Link to="/privacy">Learn more about our data sources</Link>
</p>
```

---

### 3. **Attribution Requirements** - MEDIUM PRIORITY
**Issue**: Pinterest images must be properly attributed and linked back to Pinterest.

**Current State**:
- ✅ Pinterest URLs are stored (`pinterest_url`, `pinterest_board`)
- ❓ Frontend may not be linking images back to Pinterest
- ❓ Attribution may not be clear enough

**Pinterest Requirement**:
- All Pinterest content must link back to original pin
- Clear attribution showing content is from Pinterest
- Don't obscure or cover Pinterest branding on images

**Required Fixes**:
1. **Ensure all Pinterest images are clickable** - Link to `pinterest_url`
2. **Clear attribution** - Show "Image from Pinterest" or similar
3. **Board attribution** - Show board name if available
4. **No image modification** - Don't cover Pinterest watermarks/branding

**Code to Verify**:
- `frontend/src/components/MoodboardDisplay.tsx`: Check if Pinterest images link to `pinterest_url`
- Ensure `pinterest_url` is used for clickable links

---

## ⚠️ Medium Priority Issues

### 4. **Privacy Policy Updates**
**Current State**:
- ✅ Privacy policy exists and mentions Pinterest
- ⚠️ May need clearer language about "no storage" policy

**Required Updates**:
1. **Explicitly state**: "We do NOT store Pinterest data - we call Pinterest API each time"
2. **Clarify**: Only user-generated data is stored, not Pinterest content
3. **Link prominently**: Privacy policy should be easily accessible

**Location**: `MOOREA_PRIVACY_POLICY.md` and `frontend/src/pages/PrivacyPolicy.tsx`

---

### 5. **Rate Limiting & Error Handling**
**Current State**:
- ⚠️ No visible rate limiting implementation
- ⚠️ Error handling may not be comprehensive

**Pinterest Requirement**:
- Respect rate limits
- Handle errors gracefully
- Don't spam API with requests

**Required Fixes**:
1. **Implement rate limiting** - Track API calls per user/IP
2. **Exponential backoff** - Retry with delays on rate limit errors
3. **Error logging** - Log but don't expose Pinterest API errors to users

---

## 📋 Low Priority Issues

### 6. **Terms of Service**
**Issue**: No visible Terms of Service page

**Fix**: Create Terms of Service page and link in footer

---

### 7. **API Usage Documentation**
**Issue**: No clear documentation of how Pinterest API is used

**Fix**: Document in application:
- Which endpoints are used
- How data flows through the system
- How compliance is maintained

---

## ✅ What's Already Good

1. **No Pinterest Branding** - Removed consent checkbox with Pinterest name ✅
2. **Privacy Policy Exists** - Comprehensive policy in place ✅
3. **Attribution Fields** - Backend has `pinterest_url`, `pinterest_board` fields ✅
4. **User Consent Flow** - Backend supports `pinterest_consent` parameter ✅
5. **No Image Storage** - Images are linked, not downloaded ✅

---

## 🎯 Action Plan

### Phase 1: Critical Fixes (Before Application)
1. ✅ Remove Pinterest data from cache
2. ✅ Remove Pinterest URLs from database storage
3. ✅ Add generic consent mechanism (no Pinterest branding)
4. ✅ Verify Pinterest attribution in UI

### Phase 2: Documentation (Before Application)
1. ✅ Update Privacy Policy with explicit "no storage" language
2. ✅ Create Terms of Service page
3. ✅ Document API usage in application

### Phase 3: Polish (After Application)
1. ✅ Implement rate limiting
2. ✅ Add comprehensive error handling
3. ✅ Add API usage metrics/logging

---

## 📝 Application Checklist

Before submitting Pinterest API application, ensure:

- [ ] No Pinterest data is cached
- [ ] No Pinterest URLs stored in database
- [ ] Generic user consent mechanism (no Pinterest branding)
- [ ] All Pinterest images link back to Pinterest
- [ ] Privacy Policy explicitly states "no Pinterest data storage"
- [ ] Terms of Service page exists
- [ ] Rate limiting implemented
- [ ] Error handling comprehensive
- [ ] Application clearly explains Pinterest API usage
- [ ] No misleading Pinterest branding anywhere

---

## 🔗 References

- [Pinterest Developer Guidelines](https://policy.pinterest.com/developer-guidelines)
- [Pinterest API Documentation](https://developers.pinterest.com/docs/api/v5/)

