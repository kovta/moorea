// API Response Types
export interface AestheticScore {
  name: string;
  score: number;
  description?: string;
}

export interface ImageCandidate {
  id: string;
  url: string;
  thumbnail_url?: string;
  photographer?: string;
  source_api: string;
  similarity_score?: number;
}

export enum JobStatus {
  PENDING = "pending",
  PROCESSING = "processing", 
  COMPLETED = "completed",
  FAILED = "failed"
}

export interface MoodboardResponse {
  job_id: string;
  status: JobStatus;
  message: string;
}

export interface JobStatusResponse {
  job_id: string;
  status: JobStatus;
  progress?: number;
  created_at: string;
  completed_at?: string;
  error_message?: string;
}

export interface MoodboardResult {
  job_id: string;
  status: JobStatus;
  top_aesthetics: AestheticScore[];
  images: ImageCandidate[];
  created_at: string;
  processing_time?: number;
}

// UI Component Types
export interface UploadState {
  isUploading: boolean;
  isDragActive: boolean;
  uploadedFile?: File;
}

export interface MoodboardState {
  jobId?: string;
  status: JobStatus;
  progress?: number;
  result?: MoodboardResult;
  error?: string;
}

// Authentication Types
export interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  created_at: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterCredentials {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface SavedMoodboard {
  id: number;
  title: string;
  description?: string;
  aesthetic: string;
  images: Array<{
    url: string;
    source: string;
  }>;
  user_id: number;
  created_at: string;
  updated_at: string;
}