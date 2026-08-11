import {Composition} from 'remotion';
import {PackageVideo} from './PackageVideo';
import {packageVideoSchema} from './schema';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="RogueVerseShort"
      component={PackageVideo}
      durationInFrames={1350}
      fps={30}
      width={1080}
      height={1920}
      schema={packageVideoSchema}
      calculateMetadata={({props}) => ({
        durationInFrames: Math.round(props.durationSeconds * 30),
      })}
      defaultProps={{
        title: 'RogueVerse Story',
        dek: 'Stories. Worlds. Legacies.',
        brand: 'ROGUEVERSE STUDIO',
        articleUrl: 'https://rogueversemedia.com/',
        durationSeconds: 45,
        audio: null,
        scenes: [
          {
            headline: 'The story starts here',
            body: 'A fast, visual breakdown from RogueVerse Studio.',
            image: 'site/assets/optimized/animanga-updates-1440.webp',
          },
          {
            headline: 'What changed?',
            body: 'The essential context, separated from the noise.',
            image: 'site/assets/optimized/animanga-updates-1440.webp',
          },
          {
            headline: 'The RogueVerse take',
            body: 'Read the complete story at RogueVerseMedia.com.',
            image: 'site/assets/optimized/animanga-updates-1440.webp',
          },
        ],
        captions: [],
      }}
    />
  );
};
