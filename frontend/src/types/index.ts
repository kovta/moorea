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