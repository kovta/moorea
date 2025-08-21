# API Integration Guide

This document explains how to set up and use the external image APIs integrated with the moodboard generator.

## Supported APIs

### 1. Unsplash API
**Best for**: High-quality professional photography

- **Rate Limits**: 50 requests/hour (free), 5,000/hour (demo)
- **Image Quality**: Professional, high-resolution
- **Licensing**: Free to use with attribution
- **Setup**: Get access key from [Unsplash Developers](https://unsplash.com/developers)

```bash
UNSPLASH_ACCESS_KEY=your_access_key_here
```

### 2. Pexels API  
**Best for**: Stock photography and lifestyle images

- **Rate Limits**: 200 requests/hour (free)
- **Image Quality**: Professional stock photos
- **Licensing**: Free to use, attribution appreciated
- **Setup**: Get API key from [Pexels API](https://www.pexels.com/api/)

```bash
PEXELS_API_KEY=your_api_key_here
```

### 3. Flickr API
**Best for**: Diverse community content and vintage aesthetics

- **Rate Limits**: 3,600 requests/hour (free)
- **Image Quality**: Mixed, community-generated
- **Licensing**: Creative Commons and public domain only
- **Setup**: Get API key from [Flickr App Garden](https://www.flickr.com/services/apps/create/)

```bash
FLICKR_API_KEY=your_api_key_here
```

## Content Strategy

The system queries all three APIs concurrently for each aesthetic keyword:

1. **Unsplash**: Professional lifestyle and fashion photography
2. **Pexels**: Clean stock images for modern aesthetics  
3. **Flickr**: Vintage, artistic, and alternative content

## License Compliance

### Attribution Requirements

- **Unsplash**: Photographer credit required in UI
- **Pexels**: Attribution appreciated but not mandatory
- **Flickr**: Follows individual Creative Commons licenses

### Implementation

All images include photographer attribution in the UI:

```typescript
// Frontend component automatically displays photographer credit
<Photographer>Photo by {image.photographer}</Photographer>
```

## Rate Limit Management

### Concurrent Requests
- All APIs called simultaneously per keyword
- Maximum 5 keywords processed to stay within limits
- Automatic error handling for rate limit exceeded

### Caching Strategy
- API responses cached for 24 hours
- Image embeddings cached permanently  
- Classification results cached for 7 days

## Error Handling

Each API client handles errors gracefully:

```python
# APIs that fail return empty arrays
# System continues with available results
unsplash_results = await unsplash_client.search_photos(query)  # May return []
pexels_results = await pexels_client.search_photos(query)      # May return []  
flickr_results = await flickr_client.search_photos(query)     # May return []

# Combined results from all successful APIs
all_results = unsplash_results + pexels_results + flickr_results
```

## Content Filtering

### Flickr Specific
- Only Creative Commons licensed content (licenses 4-10)
- Safe search enabled
- Photos only (no videos)

### Quality Control
- Duplicate URL removal across APIs
- Limit total candidates to 50 images
- CLIP similarity re-ranking for final selection

## Getting Started

1. **Sign up for API keys** from all three services
2. **Copy `.env.example` to `.env`** and add your keys
3. **Test individual APIs** using the `/aesthetics` endpoint
4. **Monitor rate limits** in application logs

## Production Recommendations

1. **Use paid tiers** for higher rate limits in production
2. **Implement Redis caching** for better performance  
3. **Monitor API costs** and usage patterns
4. **Consider geographic restrictions** (some APIs limited by region)
5. **Implement fallback strategies** if primary APIs fail

## Troubleshooting

### Common Issues

**"No images found"**
- Check API keys are correctly set
- Verify keywords are in English
- Check rate limits haven't been exceeded

**"API timeout"**  
- Network connectivity issues
- API service downtime
- Increase timeout in client configuration

**"Poor quality results"**
- Aesthetic keywords may need refinement
- CLIP re-ranking helps but requires good base content
- Consider adding more specific keywords to `aesthetics.yaml`