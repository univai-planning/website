---
name: caption-images
description: Audit and add captions for manually embedded images in Univ.AI markdown, QMD, and notebook content.
---

# Caption Images

Use this skill when importing or reviewing content with manually embedded
images under `posts/` or `courses/`.

## Procedure

1. Find manually embedded images.
   For markdown/QMD, search `![](` and `![...](...)`. For notebooks, inspect
   markdown cells only. Ignore generated notebook output under `*_files/`,
   `data:` URIs, card-only `image:` frontmatter, and numbered slide images.

2. View the image and read surrounding content before suggesting captions.

3. Ask the user before adding interpretive captions or citations. Suggested
   format:

   ```text
   Descriptive caption text [Source: Author or Book]
   ```

4. Apply captions.
   For markdown/QMD, edit the image alt text. For notebooks, prefer:

   ```bash
   python3 _scripts/update_captions.py <notebook> \
     --replace '![](assets/foo.png)' '![Caption](assets/foo.png)'
   ```

5. Verify no empty manual captions remain.

   ```bash
   rg -n '!\[\]\(' posts courses
   ```

## Notes

- Captions become visible Quarto figure captions when an image is alone in a
  paragraph.
- Do not invent citations. Ask or leave a follow-up.
