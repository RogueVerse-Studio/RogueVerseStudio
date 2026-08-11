import {Audio} from '@remotion/media';
import {AbsoluteFill, Series, staticFile, useVideoConfig} from 'remotion';
import {Captions} from './Captions';
import type {PackageVideoProps} from './schema';
import {ClosingScene} from './scenes/ClosingScene';
import {OpeningScene} from './scenes/OpeningScene';
import {StoryScene} from './scenes/StoryScene';

export const PackageVideo: React.FC<PackageVideoProps> = (props) => {
  const {durationInFrames, fps} = useVideoConfig();
  const openingFrames = Math.round(2.5 * fps);
  const closingFrames = Math.round(3 * fps);
  const storyFrames = Math.floor((durationInFrames - openingFrames - closingFrames) / props.scenes.length);
  const usedFrames = openingFrames + closingFrames + storyFrames * props.scenes.length;
  return (
    <AbsoluteFill style={{backgroundColor: '#080b16'}}>
      <Series>
        <Series.Sequence durationInFrames={openingFrames} name="Opening">
          <OpeningScene brand={props.brand} title={props.title} />
        </Series.Sequence>
        {props.scenes.map((scene, index) => (
          <Series.Sequence key={`${scene.headline}-${index}`} durationInFrames={storyFrames + (index === props.scenes.length - 1 ? durationInFrames - usedFrames : 0)} name={`Story ${index + 1}`}>
            <StoryScene headline={scene.headline} body={scene.body} image={scene.image} />
          </Series.Sequence>
        ))}
        <Series.Sequence durationInFrames={closingFrames} name="Closing">
          <ClosingScene url={props.articleUrl} />
        </Series.Sequence>
      </Series>
      {props.audio ? <Audio src={staticFile(props.audio)} /> : null}
      <Captions captions={props.captions} />
    </AbsoluteFill>
  );
};
