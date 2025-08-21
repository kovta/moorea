# Moodboard Generator App - Design Document

## Overview

A web application that generates aesthetic moodboards based on uploaded clothing items, similar to Pinterest's personal boards but automatically curated around identified fashion aesthetics.

## Core Concept

Upload a clothing item → AI identifies aesthetic → Generate curated moodboard with lifestyle photos, environments, and complementary items that match the aesthetic.

**Example**: Upload vintage graphic t-shirt → Identify "surfer/beach aesthetic" → Generate moodboard with surfing lifestyle, beach houses, coastal fashion, etc.

## Technical Architecture

### 1. Frontend
- **Framework**: React/Next.js
- **Features**:
  - Image upload component with drag & drop
  - Moodboard display grid (3x3 or 4x3 layout)
  - Aesthetic category display
  - Save/share functionality

### 2. Backend API
- **Framework**: Node.js/Express or Python/FastAPI
- **Core Endpoints**:
  - `POST /upload` - Process uploaded image
  - `GET /moodboard/:id` - Retrieve generated moodboard
  - `GET /aesthetics` - List available aesthetic categories

### 3. ML Pipeline - Unlimited AI Classification

**Core Approach**: CLIP zero-shot classification against comprehensive aesthetic vocabulary (200-500 terms)

1. **Aesthetic Detection**: CLIP classifies uploaded image against large vocabulary → confidence scores
2. **Keyword Expansion**: Map top aesthetic terms to search keywords via configuration file
3. **Content Fetching**: Query APIs with expanded keywords (50-100 candidates)
4. **Visual Re-ranking**: CLIP ranks candidates by similarity to original uploaded image
5. **Async Processing**: Queue-based workflow for handling multi-step pipeline

## Core Technologies

### Image Classification
- **Primary**: CLIP (Contrastive Language-Image Pre-training)
  - Via Hugging Face Transformers (`ViT-B/32` for speed/cost balance)
  - Zero-shot classification against aesthetic vocabulary
  - Image-to-image similarity for re-ranking
  - No text generation - classification only

### Content Sources (UGC APIs)
- **Primary**: Unsplash API
  - 50 requests/hour free tier
  - High-quality lifestyle photography
  - Good aesthetic diversity
- **Secondary**: Pexels API  
  - 200 requests/hour free tier
  - Backup content source
- **Future**: Pinterest API (requires business approval)

## Unlimited Aesthetic Vocabulary

**Comprehensive Dictionary (200-500 terms)**

Sources: Fashion blogs, Pinterest trends, TikTok hashtags, Instagram aesthetics

**Core Categories (Sample)**:
- **Classic**: minimalist, maximalist, vintage, retro, preppy, normcore
- **Alternative**: grunge, goth, punk, indie, emo, scene  
- **Internet Culture**: y2k, indie sleaze, coquette, that girl, clean girl, soft girl, e-girl
- **Academic**: dark academia, light academia, romantic academia
- **Lifestyle**: cottagecore, goblincore, fairycore, coastal grandmother, gorpcore
- **Urban**: streetwear, hypebeast, techwear, cyberpunk, urban minimalism
- **Bohemian**: boho, hippie, earthy, natural, witchy, spiritual

**Keyword Expansion File** (`aesthetics.yaml`):
```yaml
cottagecore:
  keywords: ["wildflower field", "rustic cabin", "vintage floral dress", "picnic basket"]
gorpcore:  
  keywords: ["hiking gear", "puffer jacket", "mountain landscape", "technical fabric"]
dark_academia:
  keywords: ["vintage library", "tweed blazer", "leather satchel", "oxford university"]
```

## Detailed Implementation Plan

### Step 1: Async Processing Architecture

```python
# Upload endpoint queues job
@app.route("/upload", methods=["POST"])
def upload_image():
    image_hash = hash_image(request.files['image'])
    job_id = queue_moodboard_job(image_hash)
    return {"job_id": job_id, "status": "processing"}

# Background worker processes job
def process_moodboard(image_hash):
    # 1. CLIP Zero-shot classification
    aesthetic_scores = clip_classify(image, aesthetic_vocabulary)
    top_aesthetics = get_top_k(aesthetic_scores, k=2)
    
    # 2. Keyword expansion
    search_keywords = []
    for aesthetic in top_aesthetics:
        keywords = aesthetics_config[aesthetic]["keywords"]
        search_keywords.extend(keywords)
    
    # 3. Fetch API candidates  
    candidates = fetch_candidates(search_keywords, limit=50)
    
    # 4. CLIP re-ranking by visual similarity
    original_embedding = clip_model.encode(uploaded_image)
    ranked_candidates = rank_by_similarity(candidates, original_embedding)
    
    # 5. Select final moodboard (top 9-12 images)
    final_moodboard = ranked_candidates[:12]
    cache_result(image_hash, final_moodboard)
```

### Step 2: CLIP Zero-Shot Classification

```python
def classify_aesthetic(image, vocabulary):
    # Prompt template for each aesthetic term
    prompts = [f"a photo of a {term} style" for term in vocabulary]
    
    # CLIP zero-shot classification
    with torch.no_grad():
        image_features = clip_model.encode_image(image)
        text_features = clip_model.encode_text(prompts)
        
        # Calculate similarities
        similarities = (100.0 * image_features @ text_features.T).softmax(dim=-1)
        
    # Return top scoring aesthetics
    return dict(zip(vocabulary, similarities[0].tolist()))
```

### Step 3: Multi-Layer Caching Strategy

```
Layer 1: Classification Cache (∞ TTL)
├── Key: sha256(uploaded_image)  
├── Value: Top aesthetic classifications
└── Purpose: Skip expensive CLIP classification

Layer 2: API Response Cache (6-24h TTL)
├── Key: "unsplash:hiking gear"  
├── Value: Raw candidate images JSON
└── Purpose: Rate limit protection

Layer 3: Image Embedding Cache (∞ TTL)  
├── Key: "img_embed:unsplash:Abc123"
├── Value: CLIP embedding vector
└── Purpose: Avoid re-encoding same images
```

## Database Schema

### Images Table
```sql
CREATE TABLE images (
    id UUID PRIMARY KEY,
    source_api VARCHAR(50), -- 'unsplash', 'pexels'  
    external_id VARCHAR(100),
    url TEXT,
    thumbnail_url TEXT,
    photographer VARCHAR(100),
    embedding VECTOR(512), -- CLIP embedding
    created_at TIMESTAMP
);
```

### Jobs Table
```sql
CREATE TABLE jobs (
    id UUID PRIMARY KEY,
    image_hash VARCHAR(64), -- SHA256 of uploaded image
    status VARCHAR(20), -- 'processing', 'completed', 'failed'
    top_aesthetics JSON, -- CLIP classification results  
    moodboard_images JSON, -- final selected image URLs
    created_at TIMESTAMP,
    completed_at TIMESTAMP
);
```

### Cache Table (optional - can use Redis instead)
```sql  
CREATE TABLE cache (
    key VARCHAR(255) PRIMARY KEY,
    value TEXT, -- JSON data
    ttl TIMESTAMP, -- expiration time
    created_at TIMESTAMP
);
```

## API Rate Limits & Costs

### Unsplash API
- **Free Tier**: 50 requests/hour  
- **Demo/Development**: 5,000 requests/hour
- **Production**: Custom pricing

### Pexels API  
- **Free Tier**: 200 requests/hour
- **No rate limit**: For approved projects

### Strategy
- Use aggressive caching to minimize API calls
- Implement background job to refresh popular aesthetic queries
- Queue system for handling traffic spikes

## Compliance & Legal

### Image Attribution
- **Unsplash**: Photographer credit required in UI
- **Pexels**: Attribution appreciated but not required  
- Store photographer info in database for proper crediting

### Terms of Service
- Both APIs allow commercial use
- Cannot redistribute images outside of app context
- Must comply with individual photographer restrictions

## Development Phases

### Phase 1: Core MVP (3-4 weeks)
- [ ] Basic image upload interface with async job queuing
- [ ] CLIP zero-shot classification pipeline  
- [ ] Initial 50 aesthetic vocabulary terms
- [ ] `aesthetics.yaml` configuration system
- [ ] Unsplash API integration with keyword search
- [ ] Image-to-image similarity re-ranking
- [ ] Job status polling endpoint

### Phase 2: Production Ready (3-4 weeks)  
- [ ] Expanded 200+ aesthetic vocabulary
- [ ] Pexels API integration as fallback  
- [ ] Multi-layer caching implementation
- [ ] Error handling and retry logic
- [ ] Basic UI for displaying moodboards
- [ ] Image attribution compliance

### Phase 3: Optimization (4-6 weeks)
- [ ] Performance monitoring and optimization
- [ ] A/B testing framework for aesthetic accuracy
- [ ] User feedback collection system
- [ ] Advanced diversity algorithms  
- [ ] Share/export functionality

## Success Metrics

### Technical KPIs
- **Aesthetic Detection Accuracy**: >75% user agreement with CLIP classifications
- **API Efficiency**: <20 API calls per moodboard (due to unlimited categories)  
- **Processing Time**: <30 seconds for complete async job
- **Cache Hit Rate**: >60% for classification, >80% for API responses

### User Experience KPIs  
- **Engagement**: >60% users interact with generated moodboard
- **Sharing**: >20% users share generated moodboards
- **Return Usage**: >30% users upload multiple images

## Risk Assessment

### Technical Risks
- **API Rate Limits**: Higher usage due to unlimited categories → aggressive caching essential
- **CLIP Classification Quality**: Unknown aesthetics may produce poor results → manual vocabulary curation
- **Search Term Mapping**: Aesthetic→keyword translation critical → requires ongoing refinement
- **Processing Time**: Multi-step async pipeline → potential bottlenecks in CLIP inference

### Business Risks  
- **API Pricing Changes**: Multiple API fallbacks planned
- **Content Licensing**: Clear attribution and ToS compliance
- **Competition**: Focus on unique aesthetic understanding

## Implementation Roadmap

### Immediate Next Steps (Week 1)
1. **Vocabulary Research**: Compile comprehensive 200+ aesthetic terms from fashion sources
2. **`aesthetics.yaml` Creation**: Map initial 50 aesthetics to search keywords
3. **Environment Setup**: Initialize FastAPI + React project with Redis/PostgreSQL
4. **CLIP Integration**: Set up Hugging Face `ViT-B/32` model pipeline
5. **Async Infrastructure**: Implement job queue system (Celery/RQ)

### Technical Foundation (Week 2-3)
1. **Zero-shot Classification**: Build CLIP aesthetic detection pipeline
2. **API Integration**: Unsplash client with rate limiting and caching
3. **Re-ranking System**: Image-to-image similarity scoring
4. **Job Management**: Status tracking and error handling
5. **Basic Frontend**: Upload interface with job polling

### MVP Launch (Week 4)
1. **Integration Testing**: End-to-end pipeline validation
2. **Performance Optimization**: Caching and bottleneck analysis
3. **UI Polish**: Moodboard display and attribution
4. **Error Handling**: Graceful failures and user feedback
5. **Initial Deployment**: Basic hosting and monitoring

---

*This design document serves as the foundational blueprint for developing the aesthetic moodboard generator. It balances technical feasibility with product vision while providing clear implementation guidance.*