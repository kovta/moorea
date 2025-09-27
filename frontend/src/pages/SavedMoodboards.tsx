import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { getUserMoodboards } from '../utils/api';
import { SavedMoodboard } from '../types';

const SavedMoodboards: React.FC = () => {
  const { token, isAuthenticated } = useAuth();
  const [moodboards, setMoodboards] = useState<SavedMoodboard[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMoodboards = async () => {
      if (!isAuthenticated || !token) {
        setIsLoading(false);
        return;
      }

      try {
        setIsLoading(true);
        setError(null);
        const savedMoodboards = await getUserMoodboards(token);
        setMoodboards(savedMoodboards);
      } catch (err: any) {
        console.error('Failed to fetch saved moodboards:', err);
        setError(err.response?.data?.detail || 'Failed to load saved moodboards.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchMoodboards();
  }, [isAuthenticated, token]);

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen gradient-bg p-4 md:p-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center py-12">
            <h1 className="text-3xl font-bold text-white mb-4">Please log in to view your saved moodboards</h1>
            <p className="text-white/80">Sign in to access your collection of saved moodboards.</p>
          </div>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="min-h-screen gradient-bg p-4 md:p-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
            <p className="text-white">Loading your saved moodboards...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen gradient-bg p-4 md:p-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center py-12">
            <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-6 rounded-lg">
              <div className="flex">
                <div className="flex-shrink-0">
                  <span className="text-red-400 text-xl">⚠️</span>
                </div>
                <div className="ml-3">
                  <p className="text-red-700 font-medium">{error}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen gradient-bg p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl sm:text-5xl md:text-6xl font-display font-bold text-white mb-4 drop-shadow-lg">
            Your Saved Moodboards
          </h1>
          <p className="text-lg md:text-xl text-white font-medium">
            {moodboards.length === 0 
              ? "No saved moodboards yet" 
              : `You have ${moodboards.length} saved moodboard${moodboards.length === 1 ? '' : 's'}`
            }
          </p>
        </div>

        {/* Moodboards Grid */}
        {moodboards.length === 0 ? (
          <div className="card max-w-2xl mx-auto text-center py-12">
            <div className="text-6xl mb-4">📋</div>
            <h2 className="text-2xl font-semibold text-gray-800 mb-3">
              No saved moodboards yet
            </h2>
            <p className="text-gray-600 mb-6">
              Create your first moodboard and save it to see it here!
            </p>
            <Link 
              to="/"
              className="btn-primary inline-flex items-center gap-2"
            >
              <span>✨</span>
              Create Your First Moodboard
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {moodboards.map((moodboard) => (
              <div key={moodboard.id} className="card hover:shadow-xl transition-all duration-200">
                {/* Moodboard Preview */}
                <div className="mb-4">
                  <div className="grid grid-cols-3 gap-1 rounded-lg overflow-hidden">
                    {/* Top row: images 1-3 */}
                    {moodboard.images.slice(1, 4).map((image, index) => (
                      <div key={index} className="aspect-square bg-gray-100">
                        <img
                          src={image.url}
                          alt={`${moodboard.title} preview ${index + 1}`}
                          className="w-full h-full object-cover"
                          loading="lazy"
                        />
                      </div>
                    ))}
                    {/* Center position - show original uploaded image */}
                    <div className="aspect-square bg-gray-100 relative">
                      {moodboard.images.length > 0 && (
                        <img
                          src={moodboard.images[0].url}
                          alt={`${moodboard.title} original`}
                          className="w-full h-full object-cover"
                          loading="lazy"
                        />
                      )}
                      {/* Add a subtle indicator that this is the original */}
                      <div className="absolute top-1 right-1 bg-white/80 rounded-full p-1">
                        <span className="text-xs">📸</span>
                      </div>
                    </div>
                    {/* Bottom row: images 4-6 */}
                    {moodboard.images.slice(4, 7).map((image, index) => (
                      <div key={index + 4} className="aspect-square bg-gray-100">
                        <img
                          src={image.url}
                          alt={`${moodboard.title} preview ${index + 4}`}
                          className="w-full h-full object-cover"
                          loading="lazy"
                        />
                      </div>
                    ))}
                  </div>
                </div>

                {/* Moodboard Info */}
                <div className="space-y-3">
                  <h3 className="text-lg font-semibold text-gray-800 line-clamp-2">
                    {moodboard.title}
                  </h3>
                  
                  {moodboard.description && (
                    <p className="text-gray-600 text-sm line-clamp-2">
                      {moodboard.description}
                    </p>
                  )}

                  <div className="flex items-center justify-between">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gradient-to-r from-purple-100 to-pink-100 text-purple-800">
                      {moodboard.aesthetic}
                    </span>
                    <span className="text-xs text-gray-500">
                      {new Date(moodboard.created_at).toLocaleDateString()}
                    </span>
                  </div>

                  <div className="pt-2 border-t border-gray-200">
                    <div className="flex justify-between items-center text-sm text-gray-600">
                      <span>{moodboard.images.length} images</span>
                      <button className="text-purple-600 hover:text-purple-800 font-medium">
                        View Full Moodboard
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Back to Home Link */}
        <div className="text-center mt-8">
          <Link 
            to="/"
            className="btn-secondary inline-flex items-center gap-2"
          >
            <span>🏠</span>
            Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
};

export default SavedMoodboards;
