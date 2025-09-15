import axios from 'axios';
import { MoodboardResponse, JobStatusResponse, MoodboardResult } from '../types';

const API_BASE = process.env.REACT_APP_API_URL || '/api/v1';

// Log the API base URL for debugging
console.log('🔧 Environment check:', {
  REACT_APP_API_URL: process.env.REACT_APP_API_URL,
  API_BASE: API_BASE,
  NODE_ENV: process.env.NODE_ENV
});

const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
});

export const uploadImage = async (file: File, envImages?: number): Promise<MoodboardResponse> => {
  console.log('🔧 API Base URL:', API_BASE);
  console.log('📁 File details:', { name: file.name, size: file.size, type: file.type });
  
  const formData = new FormData();
  formData.append('file', file);
  if (typeof envImages === 'number') {
    formData.append('env_images', String(envImages));
  }
  
  console.log('🌐 Making POST request to:', `${API_BASE}/moodboard/generate`);
  
  const response = await apiClient.post<MoodboardResponse>(
    '/moodboard/generate',
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }
  );

  console.log('📨 API Response:', response.status, response.data);
  return response.data;
};

export const getJobStatus = async (jobId: string): Promise<JobStatusResponse> => {
  const response = await apiClient.get<JobStatusResponse>(
    `/moodboard/status/${jobId}`
  );
  return response.data;
};

export const getMoodboardResult = async (jobId: string): Promise<MoodboardResult> => {
  const response = await apiClient.get<MoodboardResult>(
    `/moodboard/result/${jobId}`
  );
  return response.data;
};

export const getAesthetics = async () => {
  const response = await apiClient.get('/aesthetics');
  return response.data;
};