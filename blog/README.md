# Writing a blog post

Posts live in `blog/posts/`, one `.qmd` file each. The blog page (`blog/index.qmd`) lists them automatically, newest first. This README isn't part of the site.

## 1. Create the file

Make `blog/posts/<slug>.qmd`. The slug becomes the URL (`/blog/posts/<slug>.html`), so keep it short, lowercase and hyphenated. Start with:

```yaml
---
title: "Your title"
date: 2026-10-01
description: "One sentence shown under the title on the blog page."
draft: true
---
```

Write the post in Markdown below the front matter. Use `##` for section headings, and don't add a `#` heading: Quarto prints the title itself.

## 2. Write and preview

```
quarto preview blog/posts/<slug>.qmd
```

The page reloads each time you save. While `draft: true` is set, the post is left out of the published site and the blog listing, so unfinished posts can be committed and pushed safely.

## 3. Publish

1. Delete the `draft: true` line and set `date` to the publication date.
2. Preview once more.
3. Commit and push to `main`. The GitHub workflow rebuilds the site, and the post is live within a couple of minutes.

## Images

Put images next to the post in `blog/posts/` (or a subfolder) and reference them with a relative path: `![Alt text](figure.png)`.
