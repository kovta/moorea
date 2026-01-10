import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { MoodboardResult } from '../types';

interface MoodboardDisplayProps {
  result: MoodboardResult;
  originalImage?: File | null;
}

const MoodboardDisplay: React.FC<MoodboardDisplayProps> = ({ result, originalImage }) => {
  const [visibleImages, setVisibleImages] = useState(15); // Start with 15 images (3 rows of 5)
  const [isLoading, setIsLoading] = useState(false);
  
  // Get the dominant aesthetic (highest scoring)
  const dominantAesthetic = result.top_aesthetics[0];
  
  // Create images array with original image inserted at position 2 (third position)
  const allImages = [...result.images];
  if (originalImage) {
    const originalImageObj = {
      id: 'original-upload',
      url: URL.createObjectURL(originalImage),
      thumbnail_url: URL.createObjectURL(originalImage),
      photographer: 'You',
      source_api: 'original',
      similarity_score: 1.0 // Perfect match since it's the original
    };
    
    // Insert at position 2 (third image)
    allImages.splice(2, 0, originalImageObj);
  }
  
  // Images to display (up to the visible limit)
  const imagesToShow = allImages.slice(0, visibleImages);
  const hasMoreImages = allImages.length > visibleImages;

  const handleLoadMore = async () => {
    setIsLoading(true);
    // Simulate loading delay for better UX
    await new Promise(resolve => setTimeout(resolve, 800));
    setVisibleImages(prev => Math.min(prev + 30, allImages.length));
    setIsLoading(false);
  };

  return (
    <div className="w-full animate-fade-in">
      {/* Dominant Aesthetic Header - Always uses website color palette */}
      {dominantAesthetic && (
        <div className="text-center mb-8">
          <div 
            className="inline-flex items-center gap-3 px-6 py-3 rounded-full mb-4 shadow-md"
            style={{
              background: 'linear-gradient(135deg, #FFACAC 0%, #FFBFA9 50%, #FFEBB4 100%)'
            }}
          >
            <span className="text-2xl">✨</span>
            <div>
              <h2 className="text-lg font-semibold text-gray-800 capitalize">
                {dominantAesthetic.name.replace(/_/g, ' ')} Vibes
              </h2>
              <p className="text-sm text-gray-700 font-medium">
                {Math.round(dominantAesthetic.score * 100)}% match
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Moodboard Grid - Fixed 5 columns */}
      <div className="moodboard-grid mb-8">
        {imagesToShow.map((image, index) => {
          // Determine if image should be clickable and what link to use
          const isPinterest = image.source_api === 'pinterest';
          const linkUrl = isPinterest && image.pinterest_url 
            ? image.pinterest_url 
            : image.source_url || image.url;
          const shouldLink = isPinterest && image.pinterest_url;

          // Image content component
          const ImageContent = (
            <>
              {/* Main Image */}
              <img 
                src={image.url} 
                alt={`Moodboard inspiration ${index + 1}`}
                loading="lazy"
                className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
              />
              
              {/* Overlay that appears on hover */}
              <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <div className="absolute bottom-0 left-0 right-0 p-3">
                  {/* Source attribution - Pinterest */}
                  {isPinterest && (
                    <div className="mb-2">
                      <p className="text-white text-xs font-semibold mb-0.5 flex items-center gap-1">
                        📌 Image from Pinterest
                      </p>
                      {image.pinterest_board && (
                        <p className="text-white/80 text-xs">
                          Board: {image.pinterest_board}
                        </p>
                      )}
                      {shouldLink && (
                        <p className="text-white/70 text-xs mt-1 underline">
                          Click to view on Pinterest →
                        </p>
                      )}
                    </div>
                  )}
                  
                  {/* Photographer credit */}
                  {image.photographer && (
                    <p className="text-white text-xs font-medium mb-1">
                      📸 {image.photographer}
                    </p>
                  )}
                  
                  {/* Similarity score */}
                  {image.similarity_score && (
                    <div className="flex items-center gap-1">
                      <div className="flex-1 bg-white/20 rounded-full h-1">
                        <div 
                          className="bg-white h-1 rounded-full transition-all duration-500"
                          style={{ width: `${image.similarity_score * 100}%` }}
                        />
                      </div>
                      <span className="text-white text-xs">
                        {Math.round(image.similarity_score * 100)}%
                      </span>
                    </div>
                  )}
                </div>
              </div>

              {/* Corner indicator for high-match images */}
              {image.similarity_score && image.similarity_score > 0.8 && (
                <div className="absolute top-2 right-2 bg-gradient-to-r from-yellow-400 to-orange-400 text-white text-xs px-2 py-1 rounded-full font-medium shadow-md">
                  🔥 Hot match
                </div>
              )}

              {/* Pinterest indicator badge */}
              {isPinterest && (
                <div className="absolute top-2 left-2 bg-red-600 text-white text-xs px-2 py-1 rounded font-medium shadow-md flex items-center gap-1">
                  <span>📌</span>
                  <span>Pinterest</span>
                </div>
              )}
            </>
          );

          // Wrap in link if Pinterest image, otherwise regular div
          if (shouldLink) {
            return (
              <a
                key={image.id}
                href={linkUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="group relative aspect-square overflow-hidden rounded-lg shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1 cursor-pointer animate-fade-in block"
                style={{ animationDelay: `${index * 0.05}s` }}
                title="View on Pinterest"
              >
                {ImageContent}
              </a>
            );
          }

          return (
            <div 
              key={image.id}
              className="group relative aspect-square overflow-hidden rounded-lg shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1 cursor-pointer animate-fade-in"
              style={{ animationDelay: `${index * 0.05}s` }}
            >
              {ImageContent}
            </div>
          );
        })}
      </div>

      {/* Load More Section */}
      {hasMoreImages && (
        <div className="text-center">
          <button 
            onClick={handleLoadMore}
            disabled={isLoading}
            className="btn-primary inline-flex items-center gap-3 px-8 py-4 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <>
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                Loading more magic...
              </>
            ) : (
              <>
                <span>✨</span>
                Load More Inspiration
                <span className="bg-white/20 px-2 py-1 rounded-full text-sm">
                  +{Math.min(30, allImages.length - visibleImages)}
                </span>
              </>
            )}
          </button>
          
          <p className="text-gray-500 text-sm mt-3">
            Showing {imagesToShow.length} of {allImages.length} images
          </p>
        </div>
      )}

      {/* Fun completion message when all images are shown */}
      {!hasMoreImages && allImages.length > 12 && (
        <div className="text-center py-8">
          <div className="text-4xl mb-3">🎨</div>
          <h3 className="text-xl font-semibold text-gray-800 mb-2">
            That's all the inspiration we've got!
          </h3>
          <p className="text-gray-600">
            Hope you found some amazing style ideas for your piece ✨
          </p>
        </div>
      )}

      {/* Casual stats footer */}
      <div className="mt-12 pt-6 border-t border-gray-200 flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-gray-500">
        <div className="flex items-center gap-4">
          <span>🎯 {allImages.length} curated images</span>
          {result.processing_time && (
            <span>⚡ Generated in {result.processing_time.toFixed(1)}s</span>
          )}
        </div>
        <div className="text-xs opacity-75">
          ID: {result.job_id.toString().slice(-8)}
        </div>
      </div>

      <div className="mt-4 text-xs text-gray-400 text-center">
        <Link to="/privacy" className="underline mx-2">Privacy Policy</Link>
        <Link to="/terms" className="underline mx-2">Terms of Service</Link>
      </div>
    </div>
  );
};

export default MoodboardDisplay;