# Complete Setup Guide

This guide will help you set up and test the entire moodboard generator pipeline.

## Prerequisites

### System Requirements
- **Python 3.8+** for backend
- **Node.js 16+** for frontend  
- **Redis** for caching (optional but recommended)
- **8GB+ RAM** (CLIP model requires significant memory)
- **GPU support** (optional, for faster CLIP inference)

### API Keys Required
1. **Unsplash API**: [Get free access key](https://unsplash.com/developers)
2. **Pexels API**: [Get free API key](https://www.pexels.com/api/)
3. **Flickr API**: [Get free API key](https://www.flickr.com/services/apps/create/)

## Quick Start

### 1. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your API keys
# UNSPLASH_ACCESS_KEY=your_key_here
# PEXELS_API_KEY=your_key_here  
# FLICKR_API_KEY=your_key_here
```

### 2. Start Redis (Optional but Recommended)

```bash
# Using Docker
docker run -d -p 6379:6379 redis:alpine

# Or install locally
# macOS: brew install redis && redis-server
# Ubuntu: sudo apt install redis-server && sudo systemctl start redis
```

### 3. Start Backend

```bash
cd backend
python -m app.main
```

**Expected Output:**
```
INFO: Starting up Moodboard Generator API...
INFO: Loading CLIP model: ViT-B/32
INFO: Using device: cpu  # or cuda if GPU available
INFO: CLIP model loaded successfully  
INFO: Redis cache initialized successfully
INFO: Services initialized successfully
INFO: Uvicorn running on http://0.0.0.0:8000
```

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

**Expected Output:**
```
Compiled successfully!
Local:            http://localhost:3000
```

### 5. Test the Pipeline

1. **Open browser**: `http://localhost:3000`
2. **Upload test image**: Use any clothing image (JPEG/PNG)
3. **Monitor progress**: Watch the async processing steps
4. **View results**: See generated moodboard with aesthetic classifications

## Testing Different Scenarios

### Test Images to Try

1. **Cottagecore**: Floral dress, vintage cardigan
2. **Minimalist**: White t-shirt, simple black outfit
3. **Vintage**: 70s denim jacket, retro patterns
4. **Streetwear**: Oversized hoodie, sneakers
5. **Dark Academia**: Tweed blazer, leather satchel

### Expected Processing Flow

1. **Upload (2-3s)**: File validation and job creation
2. **CLIP Classification (5-10s)**: Aesthetic detection
3. **Keyword Expansion (1s)**: Mapping to search terms
4. **API Fetching (10-15s)**: Concurrent API calls
5. **CLIP Re-ranking (10-20s)**: Similarity scoring
6. **Result Display**: Final moodboard with 9-12 images

## Performance Optimization

### With Redis Caching
- **First request**: 30-45 seconds (full pipeline)
- **Cached request**: 2-5 seconds (using cached classification)
- **Similar aesthetics**: 10-15 seconds (cached API responses)

### Without Redis
- **Every request**: 30-45 seconds (no caching benefits)

## Troubleshooting

### Common Issues

**"CLIP model not initialized"**
```bash
# Model download issue - check internet connection
# Model loading issue - check available RAM (need 4GB+)
```

**"Redis connection failed"**
```bash
# Redis not running
redis-server

# Or disable caching by commenting Redis URL in .env
# REDIS_URL=
```

**"No images found"**
```bash
# Check API keys are correctly set in .env
# Verify rate limits not exceeded (especially Unsplash 50/hour)
# Try simpler search terms
```

**"Frontend build failed"**
```bash
# Node version too old
node --version  # Should be 16+

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Performance Issues

**Slow CLIP inference**
- Use GPU if available (install `torch` with CUDA)
- Reduce `MAX_CANDIDATES` in settings
- Use smaller CLIP model (ViT-B/16 → ViT-B/32)

**API timeouts**
- Check network connectivity
- Increase timeout in client configurations
- Reduce concurrent API calls

## Production Deployment

### Environment Variables
```bash
# Production settings
DEBUG=False
API_HOST=0.0.0.0
API_PORT=8000

# Redis (required for production)
REDIS_URL=redis://localhost:6379

# API keys (required)
UNSPLASH_ACCESS_KEY=your_production_key
PEXELS_API_KEY=your_production_key  
FLICKR_API_KEY=your_production_key

# ML optimizations
CLIP_MODEL_NAME=ViT-B/32  # or ViT-L/14 for better quality
MAX_CANDIDATES=30         # reduce for faster processing
FINAL_MOODBOARD_SIZE=9    # standard 3x3 grid
```

### Docker Deployment

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "-m", "app.main"]
```

```dockerfile  
# frontend/Dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
```

### Monitoring

**Health Checks**
- `GET /health` - Basic service health
- `GET /api/v1/aesthetics` - Verify vocabulary loading
- Redis stats via cache service

**Performance Metrics**
- CLIP inference time
- API response rates
- Cache hit ratios
- Memory usage

## Next Steps

1. **Add authentication** for user sessions
2. **Implement rate limiting** per user/IP
3. **Add image resizing** for better performance
4. **Implement job queues** with Celery for production scale
5. **Add A/B testing** for aesthetic classification accuracy
6. **Create admin dashboard** for monitoring and cache management

## Support

- Check logs in backend console
- Monitor Redis with `redis-cli monitor`
- Use browser dev tools for frontend debugging
- Post issues to project repository with logs