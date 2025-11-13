import axios from 'axios';
import { 
  MoodboardResponse, 
  JobStatusResponse, 
  MoodboardResult, 
  User, 
  LoginCredentials, 
  RegisterCredentials, 
  AuthResponse, 
  SavedMoodboard 
} from '../types';

// API_BASE should be the full base URL (e.g., https://railway-url.railway.app/api/v1)
// If REACT_APP_API_URL is set, ensure it has https:// and add /api/v1 if needed
// Otherwise, use relative path for local development
let API_BASE = '/api/v1'; // Default for local development

if (process.env.REACT_APP_API_URL) {
  let apiUrl = process.env.REACT_APP_API_URL.trim();
  
  // Add https:// if missing
  if (!apiUrl.startsWith('http://') && !apiUrl.startsWith('https://')) {
    apiUrl = `https://${apiUrl}`;
  }
  
  // Remove trailing slash if present
  apiUrl = apiUrl.replace(/\/$/, '');
  
  // Add /api/v1 if not already present
  if (!apiUrl.endsWith('/api/v1')) {
    API_BASE = `${apiUrl}/api/v1`;
  } else {
    API_BASE = apiUrl;
  }
}

// Log the API base URL for debugging
console.log('🔧 Environment check:', {
  REACT_APP_API_URL: process.env.REACT_APP_API_URL,
  API_BASE: API_BASE,
  NODE_ENV: process.env.NODE_ENV,
  isAbsolute: API_BASE.startsWith('http')
});

const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
});

export const uploadImage = async (file: File, pinterestConsent: boolean = false): Promise<MoodboardResponse> => {
  console.log('🔧 API Base URL:', API_BASE);
  console.log('📁 File details:', { name: file.name, size: file.size, type: file.type });
  console.log('📌 Pinterest consent:', pinterestConsent);
  
  const formData = new FormData();
  formData.append('file', file);
  formData.append('pinterest_consent', pinterestConsent.toString());
  
  const fullUrl = `${API_BASE}/moodboard/generate`;
  console.log('🌐 Making POST request to:', fullUrl);
  console.log('🌐 Full request URL will be:', apiClient.defaults.baseURL ? `${apiClient.defaults.baseURL}/moodboard/generate` : fullUrl);
  
  try {
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
  } catch (error: any) {
    console.error('❌ Upload error details:');
    console.error('  - Error message:', error.message);
    console.error('  - Request URL:', error.config?.url);
    console.error('  - Full request URL:', error.config?.baseURL ? `${error.config.baseURL}${error.config.url}` : error.config?.url);
    console.error('  - Status:', error.response?.status);
    console.error('  - Response data:', error.response?.data);
    throw error;
  }
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

// Authentication API functions
export const registerUser = async (credentials: RegisterCredentials): Promise<User> => {
  const response = await apiClient.post<User>('/auth/register', credentials);
  return response.data;
};

export const loginUser = async (credentials: LoginCredentials): Promise<AuthResponse> => {
  const formData = new FormData();
  formData.append('username', credentials.username);
  formData.append('password', credentials.password);
  
  const response = await apiClient.post<AuthResponse>('/auth/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  return response.data;
};

export const getCurrentUser = async (token: string): Promise<User> => {
  const response = await apiClient.get<User>('/auth/me', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  return response.data;
};

// Moodboard saving API functions
export const saveMoodboard = async (moodboard: {
  title: string;
  description?: string;
  aesthetic: string;
  images: Array<{ url: string; source: string }>;
}, token: string): Promise<SavedMoodboard> => {
  const response = await apiClient.post<SavedMoodboard>('/moodboards/', moodboard, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  return response.data;
};

export const getUserMoodboards = async (token: string): Promise<SavedMoodboard[]> => {
  const response = await apiClient.get<SavedMoodboard[]>('/moodboards/', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  return response.data;
};

// Waitlist API functions
export interface WaitlistSubscribeRequest {
  email: string;
  name?: string;
}

export interface WaitlistSubscribeResponse {
  success: boolean;
  message: string;
  email: string;
}

export const subscribeToWaitlist = async (request: WaitlistSubscribeRequest): Promise<WaitlistSubscribeResponse> => {
  const response = await apiClient.post<WaitlistSubscribeResponse>('/waitlist/subscribe', request);
  return response.data;
};