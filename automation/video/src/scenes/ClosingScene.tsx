import {AbsoluteFill, Easing, Interactive, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';

export const ClosingScene: React.FC<{url: string}> = ({url}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{alignItems: 'center', backgroundColor: '#080b16', justifyContent: 'center', padding: '120px 84px', textAlign: 'center'}}>
      <Interactive.Div name="Closing prompt" style={{color: '#ff9d27', fontFamily: 'Arial, sans-serif', fontSize: 52, fontWeight: 900, letterSpacing: 4, opacity: interpolate(frame, [0, 0.5 * fps], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.bezier(0.16, 1, 0.3, 1)})}}>
        READ THE FULL STORY
      </Interactive.Div>
      <Interactive.Div name="Article URL" style={{color: '#ffffff', fontFamily: 'Arial, sans-serif', fontSize: 64, fontWeight: 800, lineHeight: 1.12, marginTop: 42, opacity: interpolate(frame, [0.25 * fps, 0.9 * fps], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.bezier(0.16, 1, 0.3, 1)}), scale: interpolate(frame, [0.25 * fps, 0.9 * fps], [0.9, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.spring({damping: 200}), output: 'perceptual-scale'})}}>
        {url.replace('https://', '').split('/')[0]}
      </Interactive.Div>
    </AbsoluteFill>
  );
};
