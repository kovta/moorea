import React, { useState } from 'react';
import { MoodboardResult } from '../types';
import { useAuth } from '../contexts/AuthContext';
import { saveMoodboard } from '../utils/api';

interface SaveMoodboardProps {
  result: MoodboardResult;
  originalImage?: File | null;
  onSave: () => void;
}

const SaveMoodboard: React.FC<SaveMoodboardProps> = ({ result, originalImage, onSave }) => {
  const { token } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSave = async () => {
    if (!title.trim()) {
      setError('Please enter a title for your moodboard');
      return;
    }

    if (!token) {
      setError('You must be logged in to save moodboards');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      // Create images array with original image first, then generated images
      const imagesToSave = [];
      
      // Add original uploaded image first if available
      if (originalImage) {
        const originalImageUrl = URL.createObjectURL(originalImage);
        imagesToSave.push({
          url: originalImageUrl,
          source: 'original_upload',
        });
      }
      
      // Add generated moodboard images
      imagesToSave.push(...result.images.map(img => ({
        url: img.url,
        source: img.source_api,
      })));

      await saveMoodboard({
        title: title.trim(),
        description: description.trim() || undefined,
        aesthetic: result.top_aesthetics[0]?.name || 'unknown',
        images: imagesToSave,
      }, token);

      setIsOpen(false);
      setTitle('');
      setDescription('');
      onSave();
    } catch (error: any) {
      setError(error.response?.data?.detail || 'Failed to save moodboard');
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="btn-primary inline-flex items-center gap-2"
      >
        <span>💾</span>
        Save Moodboard
      </button>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-md mx-auto">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Save Moodboard</h2>
        <p className="text-gray-600">Give your moodboard a name and description</p>
      </div>

      <div className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Title *
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="e.g., My Minimalist Style"
            maxLength={100}
          />
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Optional description of your moodboard..."
            maxLength={500}
          />
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-3">
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        )}

        <div className="flex space-x-3">
          <button
            onClick={() => setIsOpen(false)}
            className="flex-1 bg-gray-200 text-gray-800 py-2 px-4 rounded-md hover:bg-gray-300 transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            disabled={isLoading}
            className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? 'Saving...' : 'Save'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default SaveMoodboard;
