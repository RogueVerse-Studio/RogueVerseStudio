import {AbsoluteFill, Easing, Interactive, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';

export const OpeningScene: React.FC<{brand: string; title: string}> = ({brand, title}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{backgroundColor: '#080b16', justifyContent: 'center', padding: '120px 84px'}}>
      <Interactive.Div name="Opening brand" style={{color: '#ff9d27', fontFamily: 'Arial, sans-serif', fontSize: 44, fontWeight: 800, letterSpacing: 8, opacity: interpolate(frame, [0, 0.5 * fps], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.bezier(0.16, 1, 0.3, 1)})}}>
        {brand}
      </Interactive.Div>
      <Interactive.Div name="Opening title" style={{color: '#ffffff', fontFamily: 'Arial, sans-serif', fontSize: 94, fontWeight: 900, lineHeight: 1.02, marginTop: 36, opacity: interpolate(frame, [0.25 * fps, 1 * fps], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.bezier(0.16, 1, 0.3, 1)}), translate: interpolate(frame, [0.25 * fps, 1 * fps], ['0px 80px', '0px 0px'], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.bezier(0.16, 1, 0.3, 1)})}}>
        {title}
      </Interactive.Div>
    </AbsoluteFill>
  );
};
