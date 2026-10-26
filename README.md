# svg-painting

A [Claude Code](https://code.claude.com) skill that lets the agent paint pictures as SVG and check its own work visually.

Instead of writing SVG blindly, the agent works in a loop, the way a human artist would:

1. creates a blank white SVG canvas,
2. adds shapes,
3. renders the SVG to a PNG with a bundled script,
4. looks at the result,
5. fixes what is wrong and repeats steps 2-4 until the picture is done.

The rendered image is what the agent judges, not the code, which is what makes the results noticeably better than one-shot SVG generation.

<!-- Add an example here: a prompt, the final PNG, and maybe a few intermediate iterations. -->

## Features

- Draw-render-look-fix loop with concrete finishing criteria and an iteration limit
- Default canvas of 1920x1080, other sizes when asked or when the subject needs it
- Zoom-in inspection of details via a temporary copy of the SVG
- Safety checks before creating files: no overwriting existing files, no name clashes with files referenced in the project, no dropping images into folders that a build or test treats specially
- Files go to the working directory unless you specify another location

## Requirements

- Claude Code with skills support
- Python 3 and `<renderer dependency>` for `scripts/render.py`
- An agent that can view images (Claude can)

## Installation

Personal install, available in all your projects:

```bash
git clone https://github.com/xenomorphed/<repo-name> ~/.claude/skills/svg-painting
pip install <renderer dependency>
```

Project install, available only in one repository:

```bash
git clone https://github.com/xenomorphed/<repo-name> .claude/skills/svg-painting
pip install <renderer dependency>
```

Claude Code watches skill directories, so the skill should be picked up without a restart. If it is not, start a new session.

## Usage

Just ask for a picture:

> Draw a lighthouse on a cliff at sunset.

Claude loads the skill on its own when the request matches its description. You can also invoke it explicitly with `/svg-painting`.

Useful things to include in a request:

- **Size:** "square, 1024x1024". The default is 1920x1080.
- **Style and palette:** "flat style, warm colors", "minimal line art".
- **Location:** "save it to `docs/img/`". Without this, files go to the current working directory.

The agent produces `<name>.svg` and `<name>.png` next to each other.

## The render script

```bash
python scripts/render.py path/to/picture.svg
```

Takes the path to an SVG and writes a PNG with the same name next to it, at the exact size of the SVG canvas. An existing PNG with that name is overwritten.

## Permissions

The skill asks the agent to run shell commands (rendering, checking for existing files, searching the project for name clashes). To avoid a confirmation prompt on every iteration, `SKILL.md` pre-approves a limited set of tools via `allowed-tools`. Review that line in the frontmatter and adjust it to your own comfort level.

## Limitations

- SVG is good for illustrations, icons, logos, and stylized scenes. It is not a replacement for photos or detailed realistic images.
- Quality depends on the model's visual feedback, so complex scenes may take several iterations. The skill stops after about 10-12 iterations without clear improvement and reports what is still imperfect.
- The SVG must be self-contained: no external images, fonts, or stylesheets.

## Contributing

Issues and pull requests are welcome. If you change the workflow, test it on a few different prompts before opening a PR.

## License

MIT, see [LICENSE](LICENSE).