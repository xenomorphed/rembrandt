---
name: rembrandt
description: Claude can now generate pictures on its own without thidr-party models and APIs
allowed-tools: Read Write Edit Bash(python *render.py *) Bash(ls *) Bash(grep *)
---

# Claude Rembrandt

This skill lets you create pictures as SVG files and visually verify them. You cannot judge an SVG by reading its code, so you work in a loop: draw, render to a raster image, look at the result, fix what is wrong, and repeat until the picture is good.

## When to use this skill

Use it when the user wants an illustration, logo, icon, scene, diagram-like artwork, pattern, or any other picture drawn as vector graphics. Do not use it for photos or raster editing, or for charts that a plotting library can generate from data.

## Core workflow

1. **Plan.** Before writing any SVG, decide on the canvas size, the subject, the composition (what goes where), and the color palette (3-6 colors). Write this plan in one short paragraph. If the request is vague, make reasonable choices and state them. Do not stall on questions.
2. **Choose location and name, and run the safety check.** Follow the section "Location, naming and safety check" below. Do not create any file before this check passes.
3. **Create a blank canvas.** Make the new `.svg` file at the chosen path, containing only a white background. The canvas size is your decision: use **1920x1080 unless the user explicitly asks for something else** (or the subject clearly demands another shape, such as a square icon or a portrait poster). Example for the default size:
   ```svg
   <svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">
     <rect width="100%" height="100%" fill="#ffffff"/>
   </svg>
   ```
   Always set `width`, `height` and a matching `viewBox`. The render script uses the canvas size as the size of the PNG, and you should think in these coordinates for the whole task.
4. **Add shapes.** Edit the file and add shapes in z-order: background first, then large forms, then medium forms, then details. Add a few related shapes per iteration rather than everything at once.
5. **Render.** Run the bundled script, passing the path to the SVG as the only argument:
   ```bash
   python scripts/render.py path/to/picture.svg
   ```
   The script writes the raster image next to the SVG with the same name and the `.png` extension (`path/to/picture.png`), at exactly the size of the SVG canvas. An existing PNG is overwritten. Paths to the script are relative to this skill's directory; use the actual location of `render.py`.
6. **Look at the result.** Open the PNG with your image viewing capability. Always look at the rendered image, never assume the SVG is correct. Compare it to the plan and the user's request.
7. **Critique and iterate.** Write down concretely what is wrong or missing, then go back to step 4 (add or edit shapes), re-render (step 5), and look again (step 6). Repeat until the picture is finished.

Steps 4 to 7 form the loop. Steps 1 to 3 happen once.

## Location, naming and safety check

The script overwrites the PNG without asking, and a new picture in the wrong place or with the wrong name can break a project. So decide where the files go and verify it before generating anything.

**Where to put the files**
- By default, put the SVG and the PNG in the **current working directory**.
- Use a different location only if the user explicitly names one. Do not decide on your own to put pictures into `assets/`, `public/`, `src/`, `static/` or similar folders, even if they look like a natural home for images.
- If the user gave an explicit path, respect it, but still run the checks below.

**Naming**
- Use a short, descriptive, lowercase name with hyphens or underscores and no spaces, e.g. `sunset-over-lake.svg`. The PNG gets the same name automatically.
- Avoid generic names that a project may already use or reference, such as `logo`, `icon`, `favicon`, `image`, `index`, `banner`, `background`, `cover`, `preview`, `thumbnail`, `output`, `test`.

**Checks before creating anything.** Run them with shell commands, do not guess:
1. **Nothing with this name exists.** Check that neither `<name>.svg` nor `<name>.png` exists at the target path (also look for the same name with other image extensions). If one exists, do not overwrite it. Choose another name, unless the user explicitly asked you to edit or replace that exact file. In that case, say which file you are about to overwrite, and if it is tracked by git with uncommitted changes, commit or back it up first or ask.
2. **The name is not referenced anywhere.** Search the project for the name, for example `grep -r "<name>" .` (skip `node_modules`, `.git`, build output). If code, config, docs, HTML, Markdown, manifests or CI files refer to a file with this name, it is not free to use.
3. **The directory is not special.** Look at what is in the target directory and what is around it. Be careful if it is processed automatically: asset pipelines and bundlers, static site generators, glob patterns such as `*.svg` or `*.png` in scripts, tests or build configs, an icon set, a directory that is packaged or deployed, a folder that tests compare against an exact list of files, or a directory with a `.gitignore` or lint rule that treats new files in a special way. If you cannot rule out that a new image there changes something, choose another place or ask the user.
4. **It will not collide with generated or system files** (build outputs, lockfiles, caches, files owned by tools).

If a check fails and no safe alternative is obvious, stop and ask the user one short question instead of taking the risk. If all checks pass, briefly state the final path in your plan and continue.

Remember that the checks cover both files: the `.svg` you create and the `.png` the script will write next to it.

## Finishing criteria

Stop when all of these hold:
- The subject is clearly recognizable at a glance.
- The composition is balanced and nothing important is cropped or off-canvas.
- Colors are coherent and there is enough contrast between the subject and the background.
- No visible artifacts: gaps between shapes that should touch, stray shapes, broken gradients, wrongly layered elements.
- The result matches what the user asked for.

Also stop, and report honestly, if about 10-12 iterations pass without clear improvement. Say what remains imperfect instead of looping forever.

## How to iterate well

- **Critique like an art director.** Check proportions, alignment, overlap order, symmetry, spacing, color harmony, and focal point. Name specific problems ("the left wing is 40px too low", not "looks off").
- **Work from coarse to fine.** First get the big shapes and the layout right, then the secondary forms, then shading and details. Do not polish details on top of a broken composition.
- **Change a few things at a time**, so you can see what each edit did. If a change made things worse, revert it.
- **Zoom in on details.** The script always renders at canvas size, so to inspect a small region, make a temporary copy of the SVG **in a temporary directory** (for example one created with `mktemp -d`), never in the project. Change only its `viewBox` to the region of interest while keeping `width` and `height` the same, and keep the same aspect ratio as the canvas, e.g. `viewBox="600 300 480 270"` on a 1920x1080 canvas shows that region at 4x. Render the copy, look at it, then delete the temporary directory. Never edit the original's `viewBox` for this.
- **Keep the file clean.** Group related shapes with `<g id="...">` and comment each group (`<!-- sky -->`, `<!-- mountains -->`). This makes later edits precise.

## SVG guidelines

- Prefer simple primitives (`rect`, `circle`, `ellipse`, `line`, `polygon`) when they are enough. Use `path` for organic forms, with cubic Béziers (`C`, `S`) for smooth curves.
- Use `<defs>` for reusable things: `linearGradient`, `radialGradient`, `clipPath`, `mask`, and `<use>` for repeated elements.
- Gradients and soft shadows give depth: `<feGaussianBlur>` works for glow and shadows, but use filters sparingly because they slow rendering and can behave differently across renderers.
- Use `transform` (`translate`, `rotate`, `scale`) to position groups instead of recomputing every coordinate.
- Use `stroke-linecap="round"` and `stroke-linejoin="round"` for friendlier shapes. Set `fill="none"` explicitly on stroked-only paths.
- Do not rely on external resources (linked images, web fonts, external CSS). Keep the SVG self-contained. If text is needed, use common generic font families (or convert important text to paths) and check the render.
- Keep the document valid XML: close all tags, escape `&` as `&amp;`, and quote all attributes.

## Common pitfalls

- Painting in the wrong order, so a background shape covers the subject. Later elements are drawn on top.
- Forgetting `fill="none"` on paths meant to be outlines.
- Malformed path data (a missing number, a wrong command letter). If the render fails or shows nothing, check the script error and validate the path.
- Coordinates that drift outside the `viewBox`.
- Missing or mismatched `width`/`height`/`viewBox`, which gives a PNG of the wrong size or a distorted picture.
- Too many tiny details that become noise at normal size. Judge the picture at the size the user will actually see.
- Skipping the safety check and overwriting an existing file, or dropping a file into a folder that a build or test treats specially.
- Declaring the work done without looking at the latest render.

## Handling render errors

If `scripts/render.py` prints an error, read it carefully. Most failures are XML syntax errors (it normally reports the line). Fix the SVG and render again. If the renderer itself is missing or broken, tell the user what is wrong instead of silently skipping the visual check.

## Output

- The final deliverables are the `.svg` file and its `.png` render, which the script already placed next to it, in the working directory unless the user specified another location. Keep both unless the user wants only one.
- Make sure no temporary files (zoom copies, scratch renders) remain in the project.
- In your final message, briefly say what you made, the full paths of the files, and any design decisions or known imperfections. Do not paste the full SVG code unless asked.