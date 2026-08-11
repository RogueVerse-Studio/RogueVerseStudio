import type {Caption} from '@remotion/captions';
import {z} from 'zod';

export const packageVideoSchema = z.object({
  title: z.string(),
  dek: z.string(),
  brand: z.string(),
  articleUrl: z.string(),
  durationSeconds: z.number().min(25).max(60),
  audio: z.string().nullable(),
  scenes: z.array(
    z.object({
      headline: z.string(),
      body: z.string(),
      image: z.string(),
    }),
  ),
  captions: z.array(
    z.object({
      text: z.string(),
      startMs: z.number(),
      endMs: z.number(),
      timestampMs: z.number().nullable(),
      confidence: z.number().nullable(),
    }),
  ),
});

export type PackageVideoProps = z.infer<typeof packageVideoSchema> & {
  captions: Caption[];
};
