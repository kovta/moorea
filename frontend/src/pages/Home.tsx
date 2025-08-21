import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import ImageUpload from '../components/ImageUpload';
import ProgressIndicator from '../components/ProgressIndicator';
import MoodboardDisplay from '../components/MoodboardDisplay';
import { uploadImage, getJobStatus, getMoodboardResult } from '../utils/api';
import { JobStatus, MoodboardState } from '../types';

const Container = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
`;

const Content = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`;

const Header = styled.div`
  text-align: center;
  color: white;
  margin-bottom: 40px;
`;

const Title = styled.h1`
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 16px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const Subtitle = styled.p`
  font-size: 20px;
  font-weight: 300;
  opacity: 0.9;
  max-width: 600px;
  margin: 0 auto;
`;

const Card = styled.div`
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  padding: 40px;
  margin-bottom: 32px;
`;

const ErrorMessage = styled.div`
  background-color: #fee;
  border: 1px solid #fcc;
  color: #c33;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 24px;
`;

const NewSessionButton = styled.button`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  margin-top: 24px;
  transition: transform 0.2s ease;

  &:hover {
    transform: translateY(-1px);
  }
`;

const Home: React.FC = () => {
  const [moodboardState, setMoodboardState] = useState<MoodboardState>({
    status: JobStatus.PENDING
  });

  const handleFileSelect = async (file: File) => {
    try {
      setMoodboardState({ status: JobStatus.PENDING });
      
      // Upload image
      const response = await uploadImage(file);
      setMoodboardState({
        jobId: response.job_id,
        status: response.status as JobStatus
      });

      // Start polling for status
      pollJobStatus(response.job_id);
    } catch (error) {
      console.error('Upload failed:', error);
      setMoodboardState({
        status: JobStatus.FAILED,
        error: 'Failed to upload image. Please try again.'
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
  };

  return (
    <Container>
      <Content>
        <Header>
          <Title>Moodboard Generator</Title>
          <Subtitle>
            Upload a clothing image and discover the aesthetic. 
            We'll create a personalized moodboard that captures the vibe.
          </Subtitle>
        </Header>

        <Card>
          {moodboardState.error && (
            <ErrorMessage>{moodboardState.error}</ErrorMessage>
          )}

          {moodboardState.status === JobStatus.PENDING && (
            <ImageUpload 
              onFileSelect={handleFileSelect}
              isUploading={false}
            />
          )}

          {(moodboardState.status === JobStatus.PROCESSING) && (
            <ProgressIndicator 
              status={moodboardState.status}
              progress={moodboardState.progress}
            />
          )}

          {moodboardState.status === JobStatus.COMPLETED && moodboardState.result && (
            <>
              <MoodboardDisplay result={moodboardState.result} />
              <NewSessionButton onClick={handleNewSession}>
                Create Another Moodboard
              </NewSessionButton>
            </>
          )}

          {moodboardState.status === JobStatus.FAILED && (
            <NewSessionButton onClick={handleNewSession}>
              Try Again
            </NewSessionButton>
          )}
        </Card>
      </Content>
    </Container>
  );
};

export default Home;