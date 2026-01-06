# Pinterest API Compliance Issues - Pre-Approval Checklist

**Date**: January 2025  
**Status**: ⚠️ **CRITICAL ISSUES IDENTIFIED**

---

## 🚨 Critical Issues (Must Fix Before Application)

### 1. **Data Storage - CLARIFICATION NEEDED** - MEDIUM PRIORITY
**Issue**: Need to verify what Pinterest allows storing for attribution purposes.

**Current Implementation**:
- ✅ **Pinterest Client** (`services/pinterest_client.py`): Does NOT use cache - calls API directly each time ✅
- ✅ **Database Storage**: Stores `pinterest_url` and `pinterest_board` when users save moodboards
- ✅ **Moodboard Results**: Pinterest pin URLs stored for linking back to original pins

**Pinterest Policy**:
> "Except for campaign analytics information accessed about your account, you may not store any information accessed through any Pinterest Materials, including the API. Instead, call the API each time you need to access information."

**Key Distinction**:
- ❌ **Violation**: Caching raw API responses, storing API response data structures
- ✅ **Likely Required**: Storing pin URLs (`pinterest_url`) for attribution and linking back to original pins
- ❓ **Gray Area**: Storing board names and metadata for attribution

**Current Status**:
- ✅ Pinterest client does NOT cache (calls API fresh each time) - **COMPLIANT**
- ✅ Pinterest URLs stored for attribution/linking - **LIKELY REQUIRED** (Pinterest requires linking back)
- ❓ Need to verify if storing `pinterest_board` name is allowed

**Required Verification**:
1. **Confirm with Pinterest**: Is storing pin URLs for attribution/linking allowed?
2. **Frontend Linking**: Ensure all Pinterest images link to `pinterest_url` (currently missing!)
3. **Database Storage**: If storing URLs is allowed, ensure they're only used for attribution

**Potential Fixes** (if needed):
- If Pinterest confirms URLs can't be stored: Don't save Pinterest images in moodboards, or fetch fresh on display
- Ensure frontend uses `pinterest_url` for clickable links (currently not implemented)

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

### 3. **Attribution Requirements - MISSING LINKS** - HIGH PRIORITY
**Issue**: Pinterest images are NOT linked back to Pinterest, which is REQUIRED for compliance.

**Current State**:
- ✅ Pinterest URLs are stored in backend (`pinterest_url`, `pinterest_board`)
- ❌ **Frontend does NOT link images to Pinterest** - Images are not clickable
- ❌ **No Pinterest attribution shown** - No indication images are from Pinterest
- ❌ **Missing source links** - `pinterest_url` exists but is not used

**Pinterest Requirement**:
- All Pinterest content MUST link back to original pin
- Clear attribution showing content is from Pinterest
- Don't obscure or cover Pinterest branding on images

**Required Fixes** (CRITICAL):
1. **Make Pinterest images clickable** - Wrap in `<a>` tag linking to `pinterest_url`
2. **Show Pinterest attribution** - Display "📌 Image from Pinterest" or similar
3. **Board attribution** - Show board name if available (`pinterest_board`)
4. **Source indicator** - Add visual indicator for Pinterest images

**Code Changes Needed**:
- `frontend/src/components/MoodboardDisplay.tsx`: 
  - Wrap Pinterest images in clickable links
  - Add Pinterest attribution in hover overlay
  - Show `pinterest_url` link when `source_api === "pinterest"`

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
1. ✅ **Verify Pinterest URL storage policy** - Confirm if storing `pinterest_url` for attribution is allowed
2. ✅ **Add Pinterest image links** - Make all Pinterest images clickable, linking to `pinterest_url` (CRITICAL)
3. ✅ **Add Pinterest attribution** - Show "Image from Pinterest" and board name in UI
4. ✅ **Add generic consent mechanism** - Generic checkbox (no Pinterest branding)

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

