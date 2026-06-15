---
name: manim
description: "Generate Manim animation code for visual math and science videos. Use this skill whenever someone asks Claude to create, write, or fix Manim code — including scene construction, mobject animation, LaTeX rendering, graph plotting, 3D scenes, camera movement, or any visual animation using the Manim library. Also trigger when the user wants to explain a concept visually with code, animate a mathematical proof, build an educational video, or produce a rendered .mp4 or .gif from Python. Trigger proactively when the conversation is clearly heading toward visual animation even if they haven't said 'Manim' yet."
---

# Manim Animation Skill

## Step 1 — Identify which version before writing any code

They are **incompatible**. Never mix imports or patterns.

| | ManimCE | ManimGL |
|---|---|---|
| Import | `from manim import *` | `from manimlib import *` |
| Install | `pip install manim` | `pip install manimgl` |
| Math class | `MathTex(r"x^2")` | `Tex(r"$x^2$")` |
| Draw outline | `Create(obj)` | `ShowCreation(obj)` |
| Camera | `self.camera.frame` | `self.frame` |
| Default scene | `Scene` | `InteractiveScene` |
| Maintained by | Community | 3Blue1Brown |
| Docs | docs.manim.community | github.com/3b1b/manim |
| Use when | Default — stable public API | Replicating 3b1b's exact style |

**Default to ManimCE** unless the user explicitly says ManimGL, shows `from manimlib import *`, or is working with 3b1b's video source code.

---

## ManimCE references

Read these when writing ManimCE code (`from manim import *`):

- `references/manimce/layout_safety.md` — **Read for every scene** — overlap helpers, frame boundary checks, layout budget, pre-render checklist
- `references/manimce/design.md` — Full design guide: palette, color-coding, typography, timing, emphasis. Read first for aesthetic guidance
- `references/manimce/mobjects.md` — VMobject, NumberLine, Axes, always-redraw, custom shapes
- `references/manimce/animations.md` — Updaters, ValueTracker, custom Animation subclass, path following
- `references/manimce/camera.md` — MovingCameraScene, ZoomedScene, 3D camera, frame manipulation
- `references/manimce/patterns.md` — Complete working examples: proof, graph, 3D surface, bar chart, equation derivation, network graph

---

## ManimGL references

Read these when writing ManimGL code (`from manimlib import *`):

- `references/manimgl/core.md` — API reference: InteractiveScene, `self.frame`, `Tex`, `ShowCreation`, `time_span`, `GlowDot`, Axes differences, what GL has that CE doesn't and vice versa
- `references/manimgl/patterns.md` — Complete working examples: basic scene, camera control, equation derivation, ValueTracker+GlowDot, `time_span`, `VShowPassingFlash`, 3D, Pythagorean proof

---

## Quick start — ManimCE

```python
from manim import *

class MyScene(Scene):
    def construct(self):
        circle = Circle(radius=1, color=BLUE)
        self.play(Create(circle))
        self.wait(1)
```

Render:
```bash
manim -pql scene.py MyScene      # preview, low quality
manim -pqh scene.py MyScene      # preview, 1080p
manim --format=gif scene.py MyScene
```

Quality flags: `-ql` (480p), `-qm` (720p), `-qh` (1080p), `-qk` (4K).

---

## Quick start — ManimGL

```python
from manimlib import *

class MyScene(InteractiveScene):
    def construct(self):
        circle = Circle()
        self.play(ShowCreation(circle))
        self.wait()
```

Render:
```bash
manimgl scene.py MyScene          # interactive window
manimgl scene.py MyScene -w       # write to file
manimgl scene.py MyScene -s       # still image
```

---

## Core concepts (both versions)

### Mobjects

Everything on screen is a `Mobject`. Key geometry:

```python
Circle(radius=1, color=BLUE)
Square(side_length=2, color=RED)
Rectangle(width=3, height=1.5)
Line(start=LEFT, end=RIGHT)
Arrow(start=ORIGIN, end=UP)
Dot(point=ORIGIN, color=WHITE)
```

Text:
```python
# ManimCE
Text("Hello world", font_size=48)
MathTex(r"\frac{d}{dx} x^2 = 2x")

# ManimGL
Text("Hello world", font_size=48)
Tex(r"$\frac{d}{dx} x^2 = 2x$")    # note $...$
```

### Positioning (both)

```python
obj.move_to(ORIGIN)
obj.shift(RIGHT * 2)
obj.next_to(other, RIGHT)
obj.to_edge(UP)
obj.to_corner(UL)
```

### Styling (both)

```python
obj.set_color(YELLOW)
obj.set_fill(BLUE, opacity=0.5)
obj.set_stroke(WHITE, width=2)
obj.scale(2)
obj.rotate(PI / 4)
```

### Grouping (both)

```python
group = VGroup(circle, square, text)
group.arrange(RIGHT, buff=0.5)
```

---

## Animations (both versions, different names)

```python
# ManimCE name — ManimGL name
Create(obj)                  # ShowCreation(obj)
self.play(FadeIn(obj))       # same
self.play(Write(text))       # same
self.play(Transform(a, b))   # same
self.play(obj.animate.shift(RIGHT * 2))   # same
self.wait(2)                 # same
```

Run simultaneously:
```python
self.play(Create(circle), FadeIn(label), run_time=2)
```

---

## Colors (both versions)

Built-in: `RED`, `BLUE`, `GREEN`, `YELLOW`, `WHITE`, `BLACK`, `ORANGE`, `PURPLE`, `PINK`, `TEAL`, `MAROON`, `GOLD`.

Shades: `RED_A` through `RED_E` (A=lightest, E=darkest).

Custom: `ManimColor("#FF6B6B")` or `rgb_to_color([1, 0.4, 0.4])`.

---

## Layout constants (both versions)

Direction vectors: `UP`, `DOWN`, `LEFT`, `RIGHT`, `ORIGIN`, `UL`, `UR`, `DL`, `DR`.

Default frame: 8 units tall, 14.22 units wide (16:9).

---

## Output files (ManimCE)

Rendered files land in `media/videos/<filename>/<quality>/`.

---

## Design principles (both versions)

Good-looking animations follow these rules. See `references/manimce/design.md` for the full guide.

- **Background:** Always `BLACK` or near-black
- **One color per concept:** pick it and use it everywhere for that concept
- **Color-code equations** with `t2c` and reuse the same map
- **Font sizes:** 72 (title), 48 (main equation), 36 (body), 30 (annotation)
- **Timing:** `self.wait()` after every significant animation
- **Progressive disclosure:** reveal piece by piece
- **De-emphasis over removal:** fade to `opacity=0.4` rather than removing

---

## Layout safety (ManimCE)

Always check elements before animating. Copy the helpers from `references/manimce/layout_safety.md` and call them throughout `construct()`. The full reference covers frame bounds, overlap detection, temporal visibility, and the pre-render checklist.
