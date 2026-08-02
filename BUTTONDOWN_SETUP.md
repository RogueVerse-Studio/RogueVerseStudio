# RogueVerse Buttondown RSS-to-email

The website signup form already adds subscribers to the `RogueVersemedia` Buttondown list. Newsletter delivery uses Buttondown's RSS-to-email feature so no API key is exposed in the static website.

## One-time Buttondown configuration

- Feed URL: `https://rogueversemedia.com/feed.xml`
- Cadence: every time a new item is detected
- Behavior: create a draft while testing, then change to send automatically
- Skip old items: on

Use this RogueVerse email template:

```django
<p style="text-align:center">
  <img src="https://rogueversemedia.com/assets/brand/studio/rogueverse-studio-wordmark.png" alt="RogueVerse Studio" width="320">
</p>
<p style="color:#ff7a18;font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase">
  {{ item.author }}
</p>
{% if item.enclosure %}
<p><img src="{{ item.enclosure }}" alt="" style="display:block;height:auto;max-width:100%;width:100%"></p>
{% endif %}
<p>{{ item.description }}</p>
<p>
  <a href="{{ item.url }}" style="background:#ff7a18;border-radius:4px;color:#07111f;display:inline-block;font-weight:700;padding:12px 18px;text-decoration:none">
    Read Full Article
  </a>
</p>
```

Buttondown uses the RSS item title for the newsletter title. The description supplies both the summary and useful inbox preview text.

## Standard RogueVerse publishing checklist

1. Publish the article at its final permanent URL.
2. Add one new `item` at the top of `feed.xml` in the same commit.
3. Use the final article URL for both `link` and `guid`. Never change that `guid` after publication.
4. Add `pubDate`, the section label in `dc:creator`, the summary in `description`, and an absolute featured-image URL in `media:content`.
5. Add the section, image, summary, and Read Full Article link to `content:encoded` for non-Buttondown RSS readers.
6. Update `lastBuildDate` and validate the XML before publishing.

Buttondown checks the feed approximately every 30 minutes. An edit that keeps the same `guid` updates the feed item without creating a duplicate newsletter.
