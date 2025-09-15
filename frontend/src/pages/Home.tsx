import React, { useState } from 'react';
import ImageUpload from '../components/ImageUpload';
import ProgressIndicator from '../components/ProgressIndicator';
import MoodboardDisplay from '../components/MoodboardDisplay';
import { uploadImage, getJobStatus, getMoodboardResult } from '../utils/api';
import { JobStatus, MoodboardState } from '../types';

const Home: React.FC = () => {
  const [moodboardState, setMoodboardState] = useState<MoodboardState>({
    status: JobStatus.PENDING
  });
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);

  const handleFileSelect = async (file: File) => {
    try {
      console.log('🚀 Starting upload for file:', file.name, 'Size:', file.size);
      setUploadedFile(file); // Store the uploaded file
      setMoodboardState({ status: JobStatus.PENDING });
      
      // Upload image
      console.log('📤 Calling uploadImage API...');
      const response = await uploadImage(file, 4);
      console.log('✅ Upload successful:', response);
      
      setMoodboardState({
        jobId: response.job_id,
        status: response.status as JobStatus
      });

      // Start polling for status
      pollJobStatus(response.job_id);
    } catch (error: any) {
      console.error('❌ Upload failed - Full error:', error);
      console.error('❌ Error message:', error.message);
      console.error('❌ Error response:', error.response?.data);
      console.error('❌ Error status:', error.response?.status);
      
      let errorMessage = 'Failed to upload image. Please try again.';
      if (error.response) {
        errorMessage = `Upload failed: ${error.response.status} - ${error.response.data?.detail || error.message}`;
      } else if (error.message) {
        errorMessage = `Upload failed: ${error.message}`;
      }
      
      setMoodboardState({
        status: JobStatus.FAILED,
        error: errorMessage
      });
    }
  };

  const pollJobStatus = async (jobId: string) => {
    let attempts = 0;
    const maxAttempts = 60; // 5 minutes max
    
    const poll = async () => {
      try {
        attempts++;
        const statusResponse = await getJobStatus(jobId);
        
        setMoodboardState(prev => ({
          ...prev,
          status: statusResponse.status as JobStatus,
          progress: statusResponse.progress
        }));

        if (statusResponse.status === JobStatus.COMPLETED) {
          // Fetch the final result
          const result = await getMoodboardResult(jobId);
          setMoodboardState(prev => ({
            ...prev,
            result
          }));
        } else if (statusResponse.status === JobStatus.FAILED) {
          setMoodboardState(prev => ({
            ...prev,
            error: statusResponse.error_message || 'Processing failed'
          }));
        } else if (statusResponse.status === JobStatus.PROCESSING && attempts < maxAttempts) {
          // Continue polling
          setTimeout(poll, 5000); // Poll every 5 seconds
        } else if (attempts >= maxAttempts) {
          setMoodboardState(prev => ({
            ...prev,
            status: JobStatus.FAILED,
            error: 'Processing timeout. Please try again.'
          }));
        }
      } catch (error) {
        console.error('Status polling failed:', error);
        if (attempts < maxAttempts) {
          setTimeout(poll, 5000);
        } else {
          setMoodboardState(prev => ({
            ...prev,
            status: JobStatus.FAILED,
            error: 'Failed to check processing status'
          }));
        }
      }
    };

    // Start polling after a short delay
    setTimeout(poll, 2000);
  };

  const handleNewSession = () => {
    setMoodboardState({ status: JobStatus.PENDING });
    setUploadedFile(null); // Clear the uploaded file for new session
  };

  return (
    <div className="min-h-screen gradient-bg p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header - Only show on initial state */}
        {moodboardState.status === JobStatus.PENDING && (
          <div className="text-center mb-8 md:mb-12 animate-fade-in px-4">
            <div className="mb-6">
              <span className="text-5xl md:text-6xl mb-4 block animate-bounce-slow">✨</span>
              <h1 className="text-3xl sm:text-4xl md:text-6xl font-display font-bold text-white mb-4 drop-shadow-lg">
                Hello! What do you need
              </h1>
              <h1 className="text-3xl sm:text-4xl md:text-6xl font-display font-bold text-gradient mb-6 drop-shadow-lg">
                inspo for today?
              </h1>
            </div>
            <p className="text-lg md:text-xl lg:text-2xl text-white/90 font-light max-w-2xl mx-auto leading-relaxed px-4">
              Drop your clothing pic and watch the magic happen ✨
              <br className="hidden sm:block"/>
              <span className="block sm:inline text-base md:text-lg text-white/70 mt-1 sm:mt-0">
                We'll find your aesthetic & create the perfect moodboard
              </span>
            </p>
          </div>
        )}

        {/* Main Content Card */}
        <div className="card max-w-4xl mx-auto animate-slide-up">
          {/* Error Message */}
          {moodboardState.error && (
            <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-6 rounded-lg animate-fade-in">
              <div className="flex">
                <div className="flex-shrink-0">
                  <span className="text-red-400 text-xl">⚠️</span>
                </div>
                <div className="ml-3">
                  <p className="text-red-700 font-medium">{moodboardState.error}</p>
                </div>
              </div>
            </div>
          )}

          {/* Upload State */}
          {moodboardState.status === JobStatus.PENDING && (
            <div className="animate-fade-in">
              <ImageUpload 
                onFileSelect={handleFileSelect}
                isUploading={false}
              />
              
              {/* Fun helper text */}
              <div className="mt-8 text-center">
                <p className="text-gray-600 text-sm mb-3">
                  💡 <strong>Pro tip:</strong> The clearer your photo, the better your moodboard!
                </p>
                <div className="flex flex-wrap justify-center gap-2 text-xs text-gray-500">
                  <span className="bg-gray-100 px-3 py-1 rounded-full">Vintage tees</span>
                  <span className="bg-gray-100 px-3 py-1 rounded-full">Elegant dresses</span>
                  <span className="bg-gray-100 px-3 py-1 rounded-full">Street style</span>
                  <span className="bg-gray-100 px-3 py-1 rounded-full">Cozy sweaters</span>
                </div>
              </div>
            </div>
          )}

          {/* Processing State */}
          {moodboardState.status === JobStatus.PROCESSING && (
            <div className="animate-fade-in">
              <ProgressIndicator 
                status={moodboardState.status}
                progress={moodboardState.progress}
              />
            </div>
          )}

          {/* Results State */}
          {moodboardState.status === JobStatus.COMPLETED && moodboardState.result && (
            <div className="animate-fade-in">
              {/* Success header */}
              <div className="text-center mb-8">
                <span className="text-4xl mb-2 block">🎉</span>
                <h2 className="text-2xl font-display font-semibold text-gray-900 mb-2">
                  Your moodboard is ready!
                </h2>
                <p className="text-gray-600">
                  Scroll through your personalized style inspiration below
                </p>
              </div>

              <MoodboardDisplay result={moodboardState.result} originalImage={uploadedFile} />
              
              <div className="text-center mt-8">
                <button 
                  onClick={handleNewSession}
                  className="btn-primary inline-flex items-center gap-2"
                >
                  <span>✨</span>
                  Create Another Moodboard
                </button>
              </div>
            </div>
          )}

          {/* Failed State */}
          {moodboardState.status === JobStatus.FAILED && (
            <div className="text-center py-12 animate-fade-in">
              <span className="text-4xl mb-4 block">😞</span>
              <h2 className="text-xl font-semibold text-gray-900 mb-3">
                Oops! Something went wrong
              </h2>
              <p className="text-gray-600 mb-6">
                Don't worry, let's try again with a different photo
              </p>
              <button 
                onClick={handleNewSession}
                className="btn-primary inline-flex items-center gap-2"
              >
                <span>🔄</span>
                Try Again
              </button>
            </div>
          )}
        </div>

        {/* Footer - Only show on completed state */}
        {moodboardState.status === JobStatus.COMPLETED && (
          <div className="text-center mt-12 text-white/70 text-sm animate-fade-in">
            <p>Made with ✨ for fashion lovers • Share your moodboard with friends!</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;