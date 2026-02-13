# Moodboard Generator - Comprehensive App Description

## Purpose

**Moodboard Generator** is an AI-powered aesthetic discovery platform that helps users find visual inspiration for clothing and fashion design. Users upload a clothing image and receive a curated moodboard of 30+ similar aesthetic images drawn from multiple sources (Unsplash, Pexels, Flickr, and Pinterest).

## How It Works

### Pipeline Architecture
1. **Aesthetic Classification**: Uses CLIP (Contrastive Language-Image Pre-training) to analyze the uploaded image and classify it across aesthetic categories (e.g., minimalist, cottagecore, maximalist, etc.)
2. **Keyword Expansion**: Intelligently generates search keywords based on identified aesthetics
3. **Multi-Source Fetching**: Simultaneously queries Unsplash, Pexels, Flickr, and Pinterest APIs for matching images
4. **Re-ranking & Selection**: Filters and ranks results by aesthetic similarity to the original image
5. **Result Display**: Shows the original image alongside 30+ ranked inspiration images in an interactive grid

## Technology Stack

- **Backend**: FastAPI (Python), CLIP ViT-B/32 (ML), Redis (caching)
- **Frontend**: React 18, TypeScript, Tailwind CSS
- **Image Sources**: Unsplash API, Pexels API, Flickr API, Pinterest API (OAuth 2.0)
- **Database**: SQLite (user auth, saved moodboards)

## Pinterest API Compliance

Our implementation meets Pinterest's developer guidelines for third-party content display:

### Requirement 1: Link Back to Pinterest Content
✅ **Compliant**: Every generated image includes a copyable source URL (visible on hover). For Pinterest images specifically, this displays the direct pin URL (`pinterest.com/pin/[pin-id]/`), allowing users to access the original content.

### Requirement 2: Clear Attribution
✅ **Compliant**: The hover overlay clearly displays:
- "📌 Image from Pinterest" label (for Pinterest-sourced images)
- Photographer/creator credit (for Unsplash/Pexels)
- Source badge in corner (Pinterest indicator)

### Requirement 3: No Content Modification
✅ **Compliant**: Images are displayed exactly as provided by the APIs. No filters, overlays, or derivative processing is applied to Pinterest content. The moodboard is purely a curation/discovery tool, not a content creation tool.

### Requirement 4: OAuth Integration
✅ **Compliant**: We use Pinterest OAuth 2.0 for API access (not bearer token authentication), following their official authentication flow. This ensures proper access control and user privacy.

## Key Features

- **Multi-source inspiration**: Aggregates from 4 image APIs for diverse results
- **User authentication**: Supports registration, login, and Pinterest OAuth
- **Save functionality**: Users can save moodboards to their account
- **Interactive grid**: 5-column responsive layout with hover overlays
- **Attribution transparency**: Clear source indication and copyable URLs for all images
- **Aesthetic matching**: Shows similarity scores per image

## Goal: Pinterest API Approval

This implementation is designed to meet Pinterest's API partnership requirements:
1. Proper attribution to source content
2. Links directing users back to Pinterest
3. Respectful content handling (no modification)
4. OAuth security best practices
5. Transparent data sourcing

By adhering to these guidelines, we aim to obtain official Pinterest API credentials for production use.
