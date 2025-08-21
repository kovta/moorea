# Moodboard Generator

AI-powered aesthetic moodboard generation from clothing images using CLIP and UGC content APIs.

## Project Structure

```
project-mood-2/
├── backend/                 # FastAPI backend
│   ├── app/                # Core application code
│   ├── models/             # Database models
│   ├── services/           # Business logic (CLIP, APIs)
│   └── config/             # Configuration files
├── frontend/               # React frontend
│   └── src/
│       ├── components/     # React components
│       ├── pages/          # Page components
│       ├── utils/          # Utility functions
│       └── types/          # TypeScript types
├── data/                   # Static data files
│   └── aesthetics.yaml     # Aesthetic vocabulary and keywords
├── cache/                  # Cache storage (local dev)
├── tests/                  # Test files
└── docs/                   # Documentation
```

## Quick Start

1. Install dependencies: `pip install -r backend/requirements.txt`
2. Start backend: `cd backend && python -m app.main`
3. Start frontend: `cd frontend && npm start`

## Core Technologies

- **Backend**: FastAPI, CLIP (Hugging Face), Redis
- **Frontend**: React, TypeScript
- **APIs**: Unsplash, Pexels
- **ML**: CLIP ViT-B/32 for aesthetic classification