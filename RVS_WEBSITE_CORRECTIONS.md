# RogueVerse Studio Website Corrections Tracker

Last updated: August 20, 2026

This file tracks visible website issues that must be corrected before a page or visual pass is considered complete. A repository change is not considered finished until the live site reflects it correctly on desktop and mobile.

## P0 — Visual publishing standard

- [ ] Replace temporary vector / schematic placeholder art with finished RogueVerse-quality illustrated imagery wherever the page is intended to use character-driven artwork.
- [ ] Use the locked RogueVerse reference lanes consistently:
  - Old Man Otaku / AniManga owned surfaces: Omo solo editorial visual language.
  - RogueVerse Studio / Our Culture: contemporary anime ensemble / studio-life visual language.
  - Community / Create: warm collaborative creator-lounge visual language.
  - Future / Tech: RogueVerse Future canon visual language, not generic icon-only panels.
- [ ] Every major category gets dedicated artwork.
- [ ] Every article header gets dedicated artwork.
- [ ] Every clickable article title/card/preview gets artwork.
- [ ] Desktop and mobile use compositions sized for the actual display slot.
- [ ] Do not mark an image correction complete until it is verified on the live URL.

## P0 — Deployment / live-site verification

- [ ] Determine why recent repository image updates are not appearing consistently on rogueversemedia.com.
- [ ] Confirm GitHub Pages is deploying the current `main` branch revision.
- [ ] Add/refresh cache-busters for changed CSS and image references where needed.
- [ ] Verify the deployed page source actually references the newest assets.
- [ ] Check desktop and mobile after each visual push instead of assuming a successful commit equals a successful deployment.

## P0 — Our Culture

Current live issue: Comics & Collectibles, Geeky Stuff, and Tech still appear as dark/blank or old-art cards instead of the requested finished illustrated category art.

- [ ] Replace the current atlas-based Comics & Collectibles artwork with a dedicated desktop image.
- [ ] Create/use a dedicated mobile Comics & Collectibles image.
- [ ] Replace the current atlas-based Geeky Stuff artwork with a dedicated desktop image.
- [ ] Create/use a dedicated mobile Geeky Stuff image.
- [ ] Replace/update Tech gateway art with a dedicated RogueVerse-quality desktop image.
- [ ] Create/use a dedicated mobile Tech gateway image.
- [ ] Recheck Movies and Games for consistency with the same finished-art standard.
- [ ] Confirm all five gateway cards display illustrated artwork at normal desktop brightness/crop.

## P0 — Future

Current live issue: the four Future subcategory cards link to `#latest` instead of opening their own editorial destinations/articles.

- [ ] Artificial Intelligence card must link to its own article/destination.
- [ ] Robotics card must link to its own article/destination.
- [ ] Space card must link to its own article/destination.
- [ ] Science card must link to its own article/destination.
- [ ] Each destination/article gets its own header image and card image.
- [ ] Replace icon/schematic-only subcategory visuals with finished RogueVerse Future imagery where the design calls for character/world art.
- [ ] Preserve the purple/midnight/electric-violet Future identity and responsive mobile crops.

## P0 — AniManga Updates / Old Man Otaku

Current live issue: several cards now show generated schematic/vector visuals, but the requested finished editorial imagery based on the locked visual references has not replaced those temporary assets yet.

- [ ] Replace temporary generated card visuals with story-specific finished imagery.
- [ ] Eastern IP coverage may use the actual relevant anime/manga/webtoon/light-novel IP editorially with proper ownership/credit treatment.
- [ ] RogueVerse-owned AniManga page/section art should use the Omo canon model and locked solo editorial visual language.
- [ ] Do not reuse one generic AniManga banner across unrelated article cards.
- [ ] Verify every visible feed card has a unique or intentionally selected story image.

## P1 — Mythra image sizing

Current issue: title-card source proportions and rendered card sizes are inconsistent.

- [ ] Lock standard Mythra shelf cover ratio to 2:3 portrait for regular Tome/title cards.
- [ ] Preferred production size: 1200 × 1800.
- [ ] Minimum practical size: 840 × 1260.
- [ ] Rebuild/replace Stranded in a Bounty Hunter World artwork. Current declared size is only 240 × 135 (16:9), which is too small and inconsistent.
- [ ] Add the same normalized title-card class/rules to Sentou.
- [ ] Ancient Gamer, SPARX: Angelkin Saga, Unmei no Gaiden, Sentou and Stranded should render inside consistent 2:3 visual frames.
- [ ] Love × Power may remain a special 9:16 featured treatment.
- [ ] Main Mythra hero may remain a wide banner treatment.
- [ ] Decide per title whether `object-fit: cover` or `contain` is appropriate, but the visible card frame must remain consistent.

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
