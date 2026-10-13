# RogueVerse Story Engine

The Story Engine converts one approved RogueVerse master concept into reusable platform deliverables while preserving a human approval gate before publication.

## Prototype

The first prototype is **For Honor: The Anime | Act I — The Fracture**.

## Source of truth

Each campaign begins with one structured story record containing:

- campaign and installment metadata
- story beats
- article angle
- 9:16 photo-carousel cards
- short-video scenes
- YouTube long-form outline
- visual identity and character/faction locks
- rights notice
- approval state

The record is not itself a publishing action. It is production input.

## Production flow

```text
Master story record
  -> article package
  -> TikTok / Instagram photo carousel
  -> YouTube Short / vertical video
  -> long-form YouTube outline
  -> artwork requirements
  -> Remotion render input
  -> approval artifact
  -> draft PR
  -> human approval
  -> publish
```

## Human gates

The Story Engine may prepare assets automatically, but it must not silently change canon or publicly publish a campaign.

Required review points:

1. **Story approval** — major story beats and canon changes.
2. **Visual approval** — recurring character designs, faction identity, rights/credit treatment, and generated artwork consistency.
3. **Publishing approval** — the final article/social package remains behind the existing RogueVerse merge/approval flow.

## Platform views

One story record can produce multiple outputs without rewriting the story separately:

### Article
Long-form canonical feature for RogueVerseMedia.com.

### Photo carousel
Typically 8–12 standalone 1080×1920 cards. Each card contains one visual beat, one headline, and concise supporting copy.

### Vertical video
25–60 second Remotion package using 3–8 scenes, compatible with the current `content-packages` automation.

### YouTube feature
A longer video outline or script derived from the same approved beats.

## Visual lock

For the For Honor prototype:

- Knights: steel, black, muted gold
- Vikings: charcoal, leather, deep crimson
- Samurai: black, dark teal, weathered steel
- Harbinger: black, violet, cold silver
- RogueVerse host cards: orange, blue, black, white
- Style: RogueVerse Simple Cinematic Anime
- Format: 1080×1920 for social cards and vertical video

The visual system should use original RogueVerse-created artwork and should not present generated material as official Ubisoft art.

## Rights language

Every prototype output must make clear that the concept is unofficial and fan-created. `For Honor` and related names, trademarks, characters, and intellectual property remain the property of Ubisoft and their respective rights holders.

## Next engineering steps

- add a JSON Schema for Story Engine records
- create a converter from Story Engine records to current content-package JSON
- add optional carousel-card export
- add image-manifest generation
- add Remotion props generation from approved images
- keep public publishing disabled until the existing approval workflow is satisfied
