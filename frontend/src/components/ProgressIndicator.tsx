import React from 'react';
import styled, { keyframes } from 'styled-components';
import { JobStatus } from '../types';

interface ProgressIndicatorProps {
  status: JobStatus;
  progress?: number;
}

const spin = keyframes`
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
`;

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
  text-align: center;
`;

const Spinner = styled.div`
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: ${spin} 1s linear infinite;
  margin-bottom: 16px;
`;

const ProgressBar = styled.div`
  width: 300px;
  height: 8px;
  background-color: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 16px;
`;

const ProgressFill = styled.div<{ progress: number }>`
  height: 100%;
  background-color: #007bff;
  width: ${props => props.progress}%;
  transition: width 0.3s ease;
`;

const StatusText = styled.div`
  font-size: 18px;
  font-weight: 500;
  color: #333;
  margin-bottom: 8px;
`;

const SubText = styled.div`
  font-size: 14px;
  color: #666;
`;

const getStatusMessage = (status: JobStatus, progress?: number): { title: string; subtitle: string } => {
  switch (status) {
    case JobStatus.PENDING:
      return {
        title: 'Starting Analysis...',
        subtitle: 'Preparing to analyze your image'
      };
    case JobStatus.PROCESSING:
      if (progress) {
        if (progress < 25) return {
          title: 'Analyzing Aesthetics',
          subtitle: 'Using AI to identify fashion styles'
        };
        if (progress < 50) return {
          title: 'Finding Keywords',
          subtitle: 'Mapping aesthetics to search terms'
        };
        if (progress < 75) return {
          title: 'Searching Images',
          subtitle: 'Finding matching content from curated sources'
        };
        return {
          title: 'Curating Selection',
          subtitle: 'Selecting the best images for your moodboard'
        };
      }
      return {
        title: 'Processing...',
        subtitle: 'Creating your personalized moodboard'
      };
    case JobStatus.COMPLETED:
      return {
        title: 'Complete!',
        subtitle: 'Your moodboard is ready'
      };
    case JobStatus.FAILED:
      return {
        title: 'Processing Failed',
        subtitle: 'Something went wrong. Please try again.'
      };
    default:
      return {
        title: 'Processing...',
        subtitle: 'Please wait'
      };
  }
};

const ProgressIndicator: React.FC<ProgressIndicatorProps> = ({ status, progress = 0 }) => {
  const { title, subtitle } = getStatusMessage(status, progress);

  return (
    <Container>
      {status === JobStatus.PROCESSING && <Spinner />}
      <StatusText>{title}</StatusText>
      <SubText>{subtitle}</SubText>
      
      {status === JobStatus.PROCESSING && (
        <ProgressBar>
          <ProgressFill progress={progress} />
        </ProgressBar>
      )}
      
      {progress > 0 && (
        <SubText>{progress}% complete</SubText>
      )}
    </Container>
  );
};

export default ProgressIndicator;