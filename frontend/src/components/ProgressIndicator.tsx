import React, { useState, useEffect } from 'react';
import { JobStatus } from '../types';

interface ProgressIndicatorProps {
  status: JobStatus;
  progress?: number;
}

const getProgressStage = (progress: number) => {
  if (progress < 25) return 'analyzing';
  if (progress < 50) return 'expanding';
  if (progress < 75) return 'fetching';
  return 'curating';
};

const getStageConfig = (stage: string) => {
  const configs = {
    analyzing: {
      emoji: '🔍',
      title: 'Analyzing your style...',
      subtitle: 'Our AI is studying the aesthetic vibes',
      bgGradient: 'from-blue-400 to-purple-500',
      tips: ['Looking for colors & patterns', 'Detecting fabric textures', 'Understanding the style']
    },
    expanding: {
      emoji: '🧠',
      title: 'Mapping the aesthetic...',
      subtitle: 'Connecting your piece to style categories',
      bgGradient: 'from-purple-500 to-pink-500',
      tips: ['Finding related keywords', 'Exploring style connections', 'Building search terms']
    },
    fetching: {
      emoji: '🌟',
      title: 'Hunting for inspiration...',
      subtitle: 'Searching through thousands of curated images',
      bgGradient: 'from-pink-500 to-orange-400',
      tips: ['Browsing fashion galleries', 'Finding lifestyle matches', 'Collecting aesthetic gems']
    },
    curating: {
      emoji: '✨',
      title: 'Perfecting your board...',
      subtitle: 'Selecting only the most inspiring matches',
      bgGradient: 'from-orange-400 to-yellow-400',
      tips: ['Ranking by similarity', 'Choosing diverse inspirations', 'Creating the perfect mix']
    }
  };
  
  return configs[stage as keyof typeof configs] || configs.analyzing;
};

const ProgressIndicator: React.FC<ProgressIndicatorProps> = ({ status, progress = 0 }) => {
  const [currentTipIndex, setCurrentTipIndex] = useState(0);
  const [animatingEmoji, setAnimatingEmoji] = useState(false);
  
  const stage = getProgressStage(progress);
  const config = getStageConfig(stage);

  // Rotate through tips every 2 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTipIndex(prev => (prev + 1) % config.tips.length);
      setAnimatingEmoji(true);
      setTimeout(() => setAnimatingEmoji(false), 300);
    }, 2000);

    return () => clearInterval(interval);
  }, [config.tips.length]);

  if (status !== JobStatus.PROCESSING) {
    return null; // Only show for processing state
  }

  return (
    <div className="flex flex-col items-center justify-center py-16 px-8 text-center animate-fade-in">
      {/* Main emoji with fun animation */}
      <div className="mb-8 relative">
        <div 
          className={`text-8xl transition-all duration-300 ${
            animatingEmoji ? 'scale-125 rotate-12' : 'scale-100 rotate-0'
          }`}
        >
          {config.emoji}
        </div>
        
        {/* Floating sparkles around the emoji */}
        <div className="absolute -top-2 -right-2 text-2xl animate-bounce" style={{ animationDelay: '0s' }}>✨</div>
        <div className="absolute -bottom-2 -left-2 text-2xl animate-bounce" style={{ animationDelay: '0.5s' }}>💫</div>
        <div className="absolute -top-2 -left-2 text-2xl animate-bounce" style={{ animationDelay: '1s' }}>⭐</div>
      </div>

      {/* Progress title */}
      <h2 className="text-2xl md:text-3xl font-display font-bold text-gray-900 mb-3">
        {config.title}
      </h2>
      
      {/* Subtitle */}
      <p className="text-gray-600 text-lg mb-8 max-w-md">
        {config.subtitle}
      </p>

      {/* Animated progress bar */}
      <div className="w-full max-w-md mb-6">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-700">Progress</span>
          <span className="text-sm font-medium text-gray-700">{progress}%</span>
        </div>
        
        <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
          <div 
            className={`h-3 bg-gradient-to-r ${config.bgGradient} rounded-full transition-all duration-700 ease-out relative`}
            style={{ width: `${progress}%` }}
          >
            {/* Shimmer effect */}
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-pulse"></div>
          </div>
        </div>
      </div>

      {/* Rotating tips */}
      <div className="bg-gray-50 rounded-2xl px-6 py-4 mb-8 min-h-[60px] flex items-center max-w-lg">
        <div className="mr-3 text-lg">💡</div>
        <p 
          key={currentTipIndex} 
          className="text-gray-700 text-sm animate-fade-in"
        >
          {config.tips[currentTipIndex]}
        </p>
      </div>

      {/* Fun loading dots */}
      <div className="flex gap-2">
        <div className="w-3 h-3 bg-purple-400 rounded-full animate-bounce"></div>
        <div className="w-3 h-3 bg-pink-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
        <div className="w-3 h-3 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
        <div className="w-3 h-3 bg-pink-400 rounded-full animate-bounce" style={{ animationDelay: '0.3s' }}></div>
        <div className="w-3 h-3 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
      </div>

      {/* Encouraging message */}
      <p className="text-gray-500 text-sm mt-6 max-w-sm">
        Hang tight! Good style takes time to curate ✨
      </p>
    </div>
  );
};

export default ProgressIndicator;