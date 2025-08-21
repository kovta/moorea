import React from 'react';
import styled from 'styled-components';
import { MoodboardResult, AestheticScore } from '../types';

interface MoodboardDisplayProps {
  result: MoodboardResult;
}

const Container = styled.div`
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
`;

const AestheticsSection = styled.div`
  margin-bottom: 32px;
`;

const SectionTitle = styled.h2`
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
`;

const AestheticsList = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
`;

const AestheticTag = styled.div<{ score: number }>`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 16px;
  background-color: ${props => `rgba(0, 123, 255, ${props.score})`};
  color: ${props => props.score > 0.5 ? 'white' : '#333'};
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
`;

const AestheticName = styled.div`
  text-transform: capitalize;
  margin-bottom: 4px;
`;

const AestheticScore = styled.div`
  font-size: 12px;
  opacity: 0.8;
`;

const ImagesGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
`;

const ImageCard = styled.div`
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  }
`;

const Image = styled.img`
  width: 100%;
  height: 250px;
  object-fit: cover;
`;

const ImageOverlay = styled.div`
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
  color: white;
  padding: 16px;
`;

const Photographer = styled.div`
  font-size: 12px;
  opacity: 0.9;
`;

const SimilarityScore = styled.div`
  font-size: 11px;
  opacity: 0.7;
  margin-top: 4px;
`;

const Stats = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  color: #666;
  margin-top: 24px;
  padding: 16px;
  background-color: #f9f9f9;
  border-radius: 8px;
`;

const MoodboardDisplay: React.FC<MoodboardDisplayProps> = ({ result }) => {
  return (
    <Container>
      <AestheticsSection>
        <SectionTitle>Detected Aesthetics</SectionTitle>
        <AestheticsList>
          {result.top_aesthetics.map((aesthetic: AestheticScore) => (
            <AestheticTag key={aesthetic.name} score={aesthetic.score}>
              <AestheticName>{aesthetic.name.replace('_', ' ')}</AestheticName>
              <AestheticScore>{Math.round(aesthetic.score * 100)}%</AestheticScore>
            </AestheticTag>
          ))}
        </AestheticsList>
      </AestheticsSection>

      <SectionTitle>Your Moodboard</SectionTitle>
      <ImagesGrid>
        {result.images.map((image) => (
          <ImageCard key={image.id}>
            <Image 
              src={image.url} 
              alt={`Moodboard image by ${image.photographer}`}
              loading="lazy"
            />
            <ImageOverlay>
              {image.photographer && (
                <Photographer>Photo by {image.photographer}</Photographer>
              )}
              {image.similarity_score && (
                <SimilarityScore>
                  Similarity: {Math.round(image.similarity_score * 100)}%
                </SimilarityScore>
              )}
            </ImageOverlay>
          </ImageCard>
        ))}
      </ImagesGrid>

      <Stats>
        <div>
          {result.images.length} images • Generated in{' '}
          {result.processing_time ? `${result.processing_time.toFixed(1)}s` : 'N/A'}
        </div>
        <div>Job ID: {result.job_id}</div>
      </Stats>
    </Container>
  );
};

export default MoodboardDisplay;