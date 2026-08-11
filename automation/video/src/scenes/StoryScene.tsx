import {AbsoluteFill, CanvasImage, Easing, Interactive, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

export const StoryScene: React.FC<{headline: string; body: string; image: string}> = ({headline, body, image}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{backgroundColor: '#080b16', overflow: 'hidden'}}>
      <CanvasImage name="Scene artwork" src={staticFile(image)} style={{height: 1920, width: 1080, objectFit: 'cover', opacity: 0.52, scale: interpolate(frame, [0, 6 * fps], [1.04, 1.14], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.linear, output: 'perceptual-scale'})}} />
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(5,8,18,.12) 0%, rgba(5,8,18,.65) 48%, rgba(5,8,18,.97) 100%)'}} />
      <AbsoluteFill style={{justifyContent: 'flex-end', padding: '120px 84px 420px'}}>
        <Interactive.Div name="Scene headline" style={{color: '#ffffff', fontFamily: 'Arial, sans-serif', fontSize: 90, fontWeight: 900, lineHeight: 1.02, opacity: interpolate(frame, [0, 0.6 * fps], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.bezier(0.16, 1, 0.3, 1)}), translate: interpolate(frame, [0, 0.6 * fps], ['0px 70px', '0px 0px'], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.bezier(0.16, 1, 0.3, 1)})}}>
          {headline}
        </Interactive.Div>
        <Interactive.Div name="Scene context" style={{color: '#e9edf7', fontFamily: 'Arial, sans-serif', fontSize: 47, fontWeight: 600, lineHeight: 1.18, marginTop: 34, opacity: interpolate(frame, [0.35 * fps, 1 * fps], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.bezier(0.16, 1, 0.3, 1)})}}>
          {body}
        </Interactive.Div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
