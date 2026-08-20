# RogueVerse Studio Website Corrections Tracker

Last updated: August 20, 2026

This file tracks visible website issues that must be corrected before a page or visual pass is considered complete. A repository change is not considered finished until the live site reflects it correctly on desktop and mobile.

## Current repository audit

The automated visual audit currently reports:

- 91 HTML pages scanned
- 72 article pages detected
- 0 article pages missing lead art
- 0 listing cards missing visual assignment
- 0 missing local image files
- 0 major landing pages without a visual hero
- 0 broken internal links
- 44 pages still using temporary/generated visual assets that require finished-art review

The two uploaded RogueVerse site/reference montages are reserved for targets that had no image at all. They are not to overwrite pages that already have an assigned image.

## P0 — Visual publishing standard

- [x] Every major page/category has an assigned image or visual hero in the repository.
- [x] Every article page has lead art assigned in the repository.
- [x] Every tracked clickable article title/card/preview has visual art assigned in the repository.
- [x] No local image references are currently missing.
- [ ] Replace temporary vector / schematic generated art with finished RogueVerse-quality illustrated imagery wherever the page is intended to use character-driven artwork.
- [ ] Use the locked RogueVerse reference lanes consistently:
  - Old Man Otaku / AniManga owned surfaces: Omo solo editorial visual language.
  - RogueVerse Studio / Our Culture: contemporary anime ensemble / studio-life visual language.
  - Community / Create: warm collaborative creator-lounge visual language.
  - Future / Tech: RogueVerse Future canon visual language, not generic icon-only panels.
- [ ] Complete finished-art review for the 44 pages still identified by `visual-audit.md` as using generated/temp visual assets.
- [ ] Desktop and mobile use compositions sized for the actual display slot.
- [ ] Do not mark an image correction complete until it is verified on the live URL.

## P0 — Deployment / live-site verification

- [ ] Determine why recent repository image updates are not appearing consistently on rogueversemedia.com.
- [x] Confirm the repository default publishing work is being committed to `main`; the visual workflow is running after visual changes.
- [x] Refresh the Our Culture stylesheet cache-buster after its image-rendering correction.
- [ ] Verify the deployed page source actually references the newest assets.
- [ ] Check desktop and mobile after each visual push instead of assuming a successful commit equals a successful deployment.

## P0 — Previously image-less pages

These were the only major landing pages identified by the automated audit as lacking visual heroes. The user-provided RogueVerse reference montage was used only here, in accordance with the instruction not to overwrite pages that already had images.

- [x] Analytics — visual hero added.
- [x] Privacy Policy — visual hero added.
- [x] Terms of Service — visual hero added.
- [x] Audit updated to recognize these hero treatments.

## P0 — Our Culture

Repository correction completed for the blank/dark card rendering problem. The failure was caused by the category card pseudo-element inheriting background properties unreliably.

- [x] Replace inherited pseudo-element background rendering with explicit `--culture-image`, `--culture-size`, and `--culture-position` variables.
- [x] Movies desktop/mobile artwork explicitly assigned.
- [x] Games desktop/mobile artwork explicitly assigned.
- [x] Comics & Collectibles atlas artwork explicitly assigned and forced to fill the visual field.
- [x] Geeky Stuff atlas artwork explicitly assigned and forced to fill the visual field.
- [x] Tech desktop/mobile artwork explicitly assigned.
- [x] Updated CSS cache-buster to `our-culture.css?v=20260820-3`.
- [ ] Replace the atlas-based Comics & Collectibles treatment with a dedicated finished desktop/mobile illustration during the finished-art pass.
- [ ] Replace the atlas-based Geeky Stuff treatment with a dedicated finished desktop/mobile illustration during the finished-art pass.
- [ ] Recheck all five cards on the live desktop/mobile site.

## P0 — Future

- [x] Artificial Intelligence card now links to `future/ai/`.
- [x] Robotics card now links to `future/robotics/`.
- [x] Space card now links to `future/space/`.
- [x] Science card now links to `future/science/`.
- [x] Four permanent Future primer articles created.
- [x] Each Future primer has its own matching lead visual using the existing Future lane art.
- [ ] Replace icon/schematic-only Future visuals with finished RogueVerse Future character/world illustrations where the final design requires them.
- [ ] Verify all four destinations on the live site.

## P0 — AniManga Updates / Old Man Otaku

- [x] No AniManga feed card is currently missing a visual assignment.
- [x] Repeated generic fallback coverage was removed from the feed structure.
- [x] Missing Haikyu 2027 article destination restored, eliminating the final broken internal link in the audit.
- [ ] Replace temporary generated card/article visuals with story-specific finished imagery.
- [ ] Eastern IP coverage may use the actual relevant anime/manga/webtoon/light-novel IP editorially with proper ownership/credit treatment.
- [ ] RogueVerse-owned AniManga page/section art should use the Omo canon model and locked solo editorial visual language.
- [ ] Verify every visible feed card has a unique or intentionally selected finished story image.

## P1 — Existing finished art promotion

The visual workflow now tries to promote already-approved artwork embedded inside an article before leaving a generated placeholder as the lead image.

- [x] Added `.github/scripts/promote_existing_article_art.py`.
- [x] Added it to the visual publishing workflow before listing-card hydration.
- [x] First automated pass reduced pages flagged for generated/temp visual review from 50 to 44.
- [ ] Continue replacing the remaining 44 temporary/generated assets with finished illustrations or approved editorial imagery.

## P1 — Mythra image sizing

- [x] Regular Mythra title cards now render inside a consistent 2:3 visual frame.
- [x] Sentou now uses the same normalized `mythra-title-card` rules as the other shelf entries.
- [x] Love × Power remains a special 9:16 featured treatment.
- [x] Main Mythra hero remains a wide banner treatment.
- [ ] Rebuild/replace the source artwork for Stranded in a Bounty Hunter World. The current source is still only 240 × 135, although it now renders inside the normalized 2:3 frame.
- [ ] Preferred future production size for regular Mythra covers: 1200 × 1800; minimum practical size: 840 × 1260.
- [ ] Verify the full shelf on desktop and mobile after deployment.

## P1 — Responsive QA

- [ ] Check 1440px+ desktop.
- [ ] Check approximately 1024px tablet/compact desktop.
- [ ] Check 768px tablet.
- [ ] Check 390–430px mobile.
- [ ] Confirm no faces, titles, logos, or focal characters are accidentally cropped.
- [ ] Confirm no black/empty visual fields caused by incorrect sprite/atlas sizing.

## Definition of done

A correction is complete only when:

1. Correct asset exists in the repository.
2. Page markup/CSS points to it.
3. Desktop and mobile variants/crops are correct.
4. Live rogueversemedia.com deployment shows the change.
5. Click targets lead to the intended destination.
6. No temporary placeholder art remains where finished artwork is required.
