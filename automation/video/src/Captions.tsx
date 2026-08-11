import {createTikTokStyleCaptions, type TikTokPage} from '@remotion/captions';
import {AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig} from 'remotion';
import {useMemo} from 'react';
import type {PackageVideoProps} from './schema';

const CaptionPage: React.FC<{page: TikTokPage}> = ({page}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const absoluteTimeMs = page.startMs + (frame / fps) * 1000;
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'flex-end', padding: '0 84px 180px'}}>
      <div style={{backgroundColor: 'rgba(5,8,18,.84)', borderRadius: 24, color: '#ffffff', fontFamily: 'Arial, sans-serif', fontSize: 52, fontWeight: 900, lineHeight: 1.08, maxWidth: 912, overflowWrap: 'break-word', padding: '24px 30px', textAlign: 'center', whiteSpace: 'pre-wrap', width: '100%'}}>
        {page.tokens.map((token) => (
          <span key={`${token.fromMs}-${token.toMs}`} style={{color: token.fromMs <= absoluteTimeMs && token.toMs > absoluteTimeMs ? '#ff9d27' : '#ffffff'}}>
            {token.text}
          </span>
        ))}
      </div>
    </AbsoluteFill>
  );
};

export const Captions: React.FC<{captions: PackageVideoProps['captions']}> = ({captions}) => {
  const {fps} = useVideoConfig();
  const {pages} = useMemo(() => createTikTokStyleCaptions({captions, combineTokensWithinMilliseconds: 1100}), [captions]);
  return (
    <AbsoluteFill>
      {pages.map((page, index) => {
        const nextPage = pages[index + 1];
        const from = Math.round((page.startMs / 1000) * fps);
        const end = Math.round(((nextPage?.startMs ?? page.startMs + 1100) / 1000) * fps);
        if (end <= from) return null;
        return (
          <Sequence key={`${page.startMs}-${index}`} from={from} durationInFrames={end - from}>
            <CaptionPage page={page} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
