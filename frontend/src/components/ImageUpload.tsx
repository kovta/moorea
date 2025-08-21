import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import styled from 'styled-components';

interface ImageUploadProps {
  onFileSelect: (file: File) => void;
  isUploading: boolean;
}

const DropzoneContainer = styled.div<{ isDragActive: boolean; isUploading: boolean }>`
  border: 2px dashed ${props => props.isDragActive ? '#007bff' : '#ddd'};
  border-radius: 8px;
  padding: 40px;
  text-align: center;
  cursor: ${props => props.isUploading ? 'default' : 'pointer'};
  background-color: ${props => {
    if (props.isDragActive) return '#f0f8ff';
    if (props.isUploading) return '#f9f9f9';
    return '#fafafa';
  }};
  transition: all 0.2s ease;

  &:hover {
    background-color: ${props => props.isUploading ? '#f9f9f9' : '#f0f8ff'};
    border-color: ${props => props.isUploading ? '#ddd' : '#007bff'};
  }
`;

const UploadText = styled.div`
  font-size: 16px;
  color: #666;
  margin-bottom: 8px;
`;

const UploadSubtext = styled.div`
  font-size: 14px;
  color: #999;
`;

const BrowseButton = styled.button`
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  margin-top: 16px;
  transition: background-color 0.2s ease;

  &:hover {
    background-color: #0056b3;
  }

  &:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
`;

const PreviewImage = styled.img`
  max-width: 200px;
  max-height: 200px;
  border-radius: 8px;
  margin-bottom: 16px;
`;

const ImageUpload: React.FC<ImageUploadProps> = ({ onFileSelect, isUploading }) => {
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0 && !isUploading) {
      const file = acceptedFiles[0];
      onFileSelect(file);
      
      // Create preview URL
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
    }
  }, [onFileSelect, isUploading]);

  const { getRootProps, getInputProps, isDragActive, open } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.webp']
    },
    maxFiles: 1,
    disabled: isUploading,
    noClick: false, // Enable clicking
    noKeyboard: false // Enable keyboard navigation
  });

  return (
    <DropzoneContainer 
      {...getRootProps()} 
      isDragActive={isDragActive}
      isUploading={isUploading}
    >
      <input {...getInputProps()} />
      
      {previewUrl && (
        <PreviewImage src={previewUrl} alt="Upload preview" />
      )}
      
      {isUploading ? (
        <>
          <UploadText>Processing your image...</UploadText>
          <UploadSubtext>Please wait while we generate your moodboard</UploadSubtext>
        </>
      ) : isDragActive ? (
        <>
          <UploadText>Drop your clothing image here</UploadText>
          <UploadSubtext>We'll create a moodboard around its aesthetic</UploadSubtext>
        </>
      ) : (
        <>
          <UploadText>Drag & drop a clothing image here</UploadText>
          <UploadSubtext>Supported: JPEG, PNG, WebP (max 10MB)</UploadSubtext>
          <BrowseButton 
            type="button" 
            onClick={(e) => {
              e.stopPropagation();
              open();
            }}
            disabled={isUploading}
          >
            Browse Files
          </BrowseButton>
        </>
      )}
    </DropzoneContainer>
  );
};

export default ImageUpload;