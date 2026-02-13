# Moodboard Generator - User Flow & How It Works

## Complete User Journey

### 1. **Authentication**
User starts at the landing page and has two options:

#### Option A: Pinterest OAuth Login
- Click "Connect with Pinterest"
- Redirected to Pinterest OAuth consent screen
- Authorizes the app to access their Pinterest account
- `AuthContext` stores the OAuth token securely
- User is now authenticated and can save moodboards to their account

#### Option B: Anonymous Access
- Skip authentication
- Generate moodboards without saving functionality
- Can still view and interact with results

---

### 2. **Image Upload**
User navigates to the Home page (moodboard generator):

- **Upload a clothing image** via drag-and-drop or file picker
- `ImageUpload` component validates the file (image format, size)
- Image preview is displayed immediately
- Backend receives the image as `multipart/form-data`

---

### 3. **CLIP Classification**
Backend initiates the aesthetic classification pipeline:

```
[User Image]
    ↓
[CLIP ViT-B/32 Model]
    ↓
[Aesthetic Scores]
    ↓
Example: {
  "name": "cottagecore",
  "score": 0.92
}, {
  "name": "minimalist",
  "score": 0.67
}, {
  "name": "maximalist",
  "score": 0.45
}
```

- **CLIP** (Contrastive Language-Image Pre-training) analyzes visual features
- Compares the image against predefined aesthetic categories (loaded from `aesthetics.yaml`)
- Returns top 5-10 aesthetics with confidence scores (0-1)
- Highest scorer becomes the "dominant aesthetic"

**Status Update**: Frontend shows progress bar at 25%

---

### 4. **Keyword Expansion**
Backend generates search keywords from the classified aesthetics:

- For each top aesthetic, expand to related search terms
- Example: "cottagecore" → ["cottagecore dress", "prairie style", "floral vintage", "rustic aesthetic", ...]
- Apply **negative keywords** to filter out irrelevant results (e.g., avoid "sporty" for cottagecore)
- Goal: 20-40 diverse search queries to maximize candidate diversity

**Status Update**: Frontend shows progress bar at 50%

---

### 5. **Multi-Source Candidate Fetching**
Backend simultaneously queries 4 image APIs using the generated keywords:

#### API Queries (Parallel):
```
┌─ Unsplash API
│  └─ Returns: High-quality user photography
│
├─ Pexels API
│  └─ Returns: Free stock photography
│
├─ Flickr API
│  └─ Returns: Community photography
│
└─ Pinterest API (OAuth)
   └─ Returns: Curated pins if user consented
```

**Data Collected Per Image**:
- `url` (image link)
- `source_api` (which API it came from)
- `photographer` (credit)
- `source_url` (link to original source)
- `pinterest_url` (if from Pinterest)
- `pinterest_board` (if from Pinterest)

**Result**: ~150-200 candidate images aggregated

**Status Update**: Frontend shows progress bar at 75%

---

### 6. **Re-ranking & Filtering**
Backend filters and re-ranks candidates:

- Remove duplicates/near-duplicates (pixel hash comparison)
- Re-run CLIP to score each candidate against the original image
- Calculate **similarity_score** (0-1) for each image
- Sort by similarity score (highest first)
- Select top 30-40 images for display

---

### 7. **Moodboard Display**
Frontend receives the completed moodboard result and renders it:

#### Result JSON Structure:
```json
{
  "job_id": "a1b2c3d4...",
  "status": "completed",
  "top_aesthetics": [
    { "name": "cottagecore", "score": 0.92 },
    { "name": "romantic", "score": 0.78 }
  ],
  "images": [
    {
      "id": "pin_12345",
      "url": "https://...",
      "source_api": "pinterest",
      "similarity_score": 0.94,
      "photographer": "Jane Doe",
      "pinterest_url": "https://pinterest.com/pin/12345/",
      "pinterest_board": "Fashion Inspo"
    },
    {
      "id": "unsplash_67890",
      "url": "https://...",
      "source_api": "unsplash",
      "similarity_score": 0.89,
      "photographer": "John Smith",
      "source_url": "https://unsplash.com/photos/..."
    }
    // ... 28+ more images
  ],
  "processing_time": 8.5
}
```

#### Grid Display:
- **5-column responsive grid** (Tailwind CSS)
- **Original uploaded image** inserted at position 3 (to show the inspiration source)
- Images ranked by similarity score (highest quality matches first)
- Each image shows:
  - Thumbnail with scale animation on hover
  - Similarity score as progress bar
  - "🔥 Hot match" badge for images with >80% similarity
  - Source API badge (e.g., "📌 Pinterest")

**Status Update**: Frontend transitions to 100% - "Moodboard Ready"

---

### 8. **Hover Overlay Interaction**
When user hovers over an image:

Overlay appears with:
- **Source attribution**: "📌 Image from Pinterest" (if Pinterest)
- **Photographer credit**: "📸 John Smith"
- **Board name**: "Board: Fashion Inspo" (if Pinterest)
- **Similarity score**: Visual bar showing match percentage
- **Copyable source URL**: Plain text at bottom (pale white, selectable)
  - For Pinterest: `https://pinterest.com/pin/[id]/`
  - For Unsplash/Pexels: Direct link to the original photo page

**User can**: Click-to-copy or manually select the URL to visit the source

---

### 9. **Save Moodboard (Authenticated Users Only)**
If user is logged in via Pinterest OAuth:

- Click **"Save This Moodboard"** button
- `SaveMoodboard` modal appears:
  - Input title (auto-suggested: dominant aesthetic name)
  - Optional description
  - Confirm save
- Backend stores:
  - Moodboard metadata (title, description, aesthetic)
  - All 30+ image URLs and metadata
  - Timestamp, user_id, job_id
- User can later access saved moodboards from `/saved` page

---

### 10. **View Saved Moodboards**
Authenticated users can:

- Navigate to `/saved`
- View all their previously generated moodboards
- See dominant aesthetic, creation date, image count
- Regenerate or delete moodboards
- Share moodboard links (future feature)

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ FRONTEND (React)                                                │
├─────────────────────────────────────────────────────────────────┤
│  1. User uploads image via ImageUpload component                │
│  2. Shows progress indicator (0% → 100%)                        │
│  3. Displays final moodboard in 5-column grid                   │
│  4. Enables save/share functionality if authenticated            │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP POST /generate
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ BACKEND (FastAPI)                                               │
├─────────────────────────────────────────────────────────────────┤
│  1. Receive image bytes → create job in database                │
│  2. CLIP classify aesthetics (25%)                              │
│  3. Expand keywords from aesthetics (50%)                       │
│  4. Parallel API calls (Unsplash, Pexels, Flickr, Pinterest)    │
│  5. CLIP re-rank each candidate (75%)                           │
│  6. Select top 30-40 by similarity score (100%)                 │
│  7. Return job_id + results                                     │
└────────────────────────────┬────────────────────────────────────┘
                             │ JSON response
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│ FRONTEND (continued)                                            │
├─────────────────────────────────────────────────────────────────┤
│  Render MoodboardDisplay component with results                 │
│  User can hover/save/share                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Technical Decisions

### Why This Architecture?

1. **Multi-source APIs**: No single API (including Pinterest) provides comprehensive fashion imagery. Aggregating ensures quality diversity.

2. **CLIP for Classification**: Language-free aesthetic recognition works across visual styles without explicit tagging. Better than keyword-matching alone.

3. **Two-pass CLIP**: First pass identifies aesthetics from user's image → keywords generated → second pass scores candidates against original image for ranking.

4. **OAuth for Pinterest**: Respects user privacy and follows Pinterest's official authentication flow. Enables saved moodboards tied to user accounts.

5. **Hover-only URLs**: Keeps UI clean while ensuring attribution is available. Copyable (not clickable) respects Pinterest's design guidelines.

6. **Redis caching**: Speeds up repeated searches by caching CLIP embeddings and API responses.

---

## Summary

**User Path**:
```
Login (optional) → Upload → Classify → Expand Keywords → Fetch → Rank → Display → Interact → Save
```

**Processing Time**: ~8-10 seconds end-to-end (mostly CLIP inference + API calls)

**Result**: 30+ curated inspiration images with clear attribution and copyable source URLs for every image.
