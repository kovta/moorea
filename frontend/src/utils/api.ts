import axios from 'axios';
import { MoodboardResponse, JobStatusResponse, MoodboardResult } from '../types';

const API_BASE = '/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
});

export const uploadImage = async (file: File): Promise<MoodboardResponse> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await apiClient.post<MoodboardResponse>(
    '/moodboard/generate',
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }
  );

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