import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';

interface ImageUploadProps {
  onFileSelect: (file: File, pinterestConsent: boolean) => void;
  isUploading: boolean;
}

const ImageUpload: React.FC<ImageUploadProps> = ({ onFileSelect, isUploading }) => {
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [pinterestConsent, setPinterestConsent] = useState<boolean>(false);

  const onDrop = useCallback((acceptedFiles: File[], rejectedFiles: any[]) => {
    if (rejectedFiles.length > 0) {
      // Handle rejected files
      const rejectedFile = rejectedFiles[0];
      console.error('❌ File rejected:', rejectedFile.file.name, rejectedFile.errors);
      alert(`File "${rejectedFile.file.name}" is not supported. Please use JPEG, PNG, or WebP format.`);
      return;
    }
    
    if (acceptedFiles.length > 0 && !isUploading) {
      const file = acceptedFiles[0];
      console.log('✅ File accepted:', file.name, file.type);
      onFileSelect(file, pinterestConsent);
      
      // Create preview URL
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
    }
  }, [onFileSelect, isUploading, pinterestConsent]);

  const { getRootProps, getInputProps, isDragActive, open } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.webp']
    },
    maxFiles: 1,
    disabled: isUploading,
    noClick: false,
    noKeyboard: false
  });

  // Dynamic classes based on state
  const getContainerClasses = () => {
    let baseClasses = "relative border-2 border-dashed rounded-2xl p-8 md:p-12 text-center transition-all duration-300 ease-in-out";
    
    if (isUploading) {
      return `${baseClasses} border-gray-300 bg-gray-50 cursor-default`;
    } else if (isDragActive) {
      return `${baseClasses} border-purple-400 bg-purple-50 cursor-pointer transform scale-105 shadow-lg`;
    } else {
      return `${baseClasses} border-gray-300 bg-gray-50 hover:border-purple-400 hover:bg-purple-50 cursor-pointer hover:shadow-lg hover:-translate-y-1`;
    }
  };

  return (
    <div 
      {...getRootProps()} 
      className={getContainerClasses()}
    >
      <input {...getInputProps()} />
      
      {/* Upload Icon */}
      <div className="mb-6">
        {isDragActive ? (
          <div className="text-6xl animate-bounce">📸</div>
        ) : isUploading ? (
          <div className="text-6xl animate-pulse">⏳</div>
        ) : (
          <div className="text-6xl animate-float">👔</div>
        )}
      </div>

      {/* Preview Image */}
      {previewUrl && !isUploading && (
        <div className="mb-6">
          <img 
            src={previewUrl} 
            alt="Upload preview" 
            className="max-w-48 max-h-48 mx-auto rounded-xl shadow-md border-2 border-white"
          />
        </div>
      )}
      
      {/* Content based on state */}
      {isUploading ? (
        <div className="animate-fade-in">
          <h3 className="text-xl font-semibold text-gray-700 mb-2">
            ✨ Analyzing your style...
          </h3>
          <p className="text-gray-600">
            Our AI is detecting the aesthetic and curating your moodboard
          </p>
          <div className="mt-4 flex justify-center items-center gap-1">
            <div className="w-2 h-2 rounded-full animate-bounce" style={{ backgroundColor: '#FFE99A', animationDelay: '0s' }}></div>
            <div className="w-2 h-2 rounded-full animate-bounce" style={{ backgroundColor: '#FFD586', animationDelay: '0.1s' }}></div>
            <div className="w-2 h-2 rounded-full animate-bounce" style={{ backgroundColor: '#FFAAAA', animationDelay: '0.2s' }}></div>
          </div>
        </div>
      ) : isDragActive ? (
        <div className="animate-fade-in">
          <h3 className="text-xl font-semibold text-purple-700 mb-2">
            Perfect! Drop it right here ✨
          </h3>
          <p className="text-purple-600">
            We'll instantly create a moodboard around your piece
          </p>
        </div>
      ) : (
        <div className="animate-fade-in">
          <h3 className="text-xl md:text-2xl font-semibold text-gray-800 mb-3">
            Drop your fashion pic here
          </h3>
          <p className="text-gray-600 mb-6 max-w-md mx-auto">
            We support PNG, JPEG, WebP
          </p>
          
          {/* Browse Button */}
          <button 
            type="button" 
            onClick={(e) => {
              e.stopPropagation();
              open();
            }}
            disabled={isUploading}
            className="btn-primary inline-flex items-center gap-2 text-base px-8 py-3"
          >
            Choose from Gallery
          </button>

        </div>
      )}

      {/* Subtle upload indicator for large files */}
      <div className="absolute top-4 right-4">
        {isDragActive && (
          <div className="bg-purple-500 text-white px-3 py-1 rounded-full text-xs font-medium animate-pulse">
            Ready!
          </div>
        )}
      </div>
    </div>
  );
};

export default ImageUpload;