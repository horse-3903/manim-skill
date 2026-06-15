<div align="center">

# manim-skill

Claude Code skill for generating Manim Community Edition animation code

[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![Manim](https://img.shields.io/badge/ManimCE-stable-orange?style=flat-square)](https://docs.manim.community)

</div>

---

## Demo animations

Generated entirely by Claude using this skill, no manual Manim code written.

![Linear Regression](demos/linear_regression/LinearRegressionScene.gif)

---

## Overview

**manim-skill** is a Claude Code skill that gives Claude the knowledge to generate correct, renderable [ManimCE](https://docs.manim.community) animation code. 

It covers the full surface area of Manim: scenes, mobjects, animations, LaTeX, graph plotting, 3D scenes, camera movement, and complete working examples for math and science visualizations.

## Skills

| Install name | Description |
|---|---|
| `manim` | ManimCE scene structure, mobjects, animations, LaTeX, graphs, 3D, camera, and patterns |

---

## Installation

### Option 1: npx (recommended)

```bash
npx skills add https://github.com/horse-3903/manim-skill
```

Install the skill by name:

```bash
npx skills add https://github.com/horse-3903/manim-skill --skill "manim"
```

### Option 2: Claude Code plugin

```bash
claude plugin add https://github.com/horse-3903/manim-skill
```

### Option 3: Copy SKILL.md directly

Copy the contents of [`skills/manim/SKILL.md`](skills/manim/SKILL.md) into your project's `.claude/` directory, your `CLAUDE.md` file, or paste directly into a Claude conversation.

### Option 4: Manual local install

```bash
git clone https://github.com/horse-3903/manim-skill
cd manim-skill

# Get the path to the skill
./skill.sh manim
# -> skills/manim/SKILL.md

# Copy into your project
cp -r skills/manim your-project/.claude/skills/
```

---

## For AI Agents: Automated Installation

```bash
# 1. Clone the repo
git clone https://github.com/horse-3903/manim-skill /tmp/manim-skill

# 2. Copy the skill into the user's project
mkdir -p .claude/skills
cp -r /tmp/manim-skill/skills/manim .claude/skills/

# 3. Verify
ls .claude/skills/manim/SKILL.md
```

---

## What's in the skill

**`skills/manim/SKILL.md`** - triggers on any Manim animation conversation and covers:

- ManimCE vs ManimGL distinction (imports, install, when to use each)
- Core scene structure and render commands
- Mobjects: geometry, text, LaTeX, positioning, styling, VGroup
- Animations: Create, Write, Transform, ReplacementTransform, `.animate` syntax
- Common patterns: Indicate, Circumscribe, Axes, graph plotting, updaters, ValueTracker
- 3D scenes with ThreeDScene
- Color constants and layout coordinate system

**`skills/manim/references/`** - read on demand:

| File | Contents |
|---|---|
| `mobjects.md` | VMobject internals, NumberLine, Axes, always_redraw, Table, MathTex internals, SVG/Image |
| `animations.md` | ValueTracker, updaters, custom Animation subclass, MoveAlongPath, rate functions, LaggedStart |
| `camera.md` | MovingCameraScene, ZoomedScene, 3D camera, ThreeDScene, ambient rotation, config flags |
| `patterns.md` | 6 complete runnable examples: Pythagorean proof, function explorer, 3D surface, bar chart, equation derivation, graph network |

---

## Project Structure

```
manim-skill/
├── .claude-plugin/
│   ├── plugin.json          # Claude Code plugin metadata
│   └── marketplace.json     # Marketplace listing
├── skills/
│   ├── llms.txt             # One-line descriptions for all skills
│   └── manim/
│       ├── SKILL.md         # Main skill (triggers + core patterns)
│       └── references/
│           ├── mobjects.md
│           ├── animations.md
│           ├── camera.md
│           └── patterns.md
├── skill.sh                 # Local helper, prints path to a skill's SKILL.md
├── LICENSE
└── README.md
```

---

## License

MIT
