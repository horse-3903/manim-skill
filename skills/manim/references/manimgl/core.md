# ManimGL: Core API Reference

ManimGL is Manim maintained by 3Blue1Brown, used in all 3b1b YouTube videos.

**Import:** `from manimlib import *`
**Install:** `pip install manimgl`
**Run:** `manimgl scene.py SceneName`

---

## Scene classes

| Class | Use when |
|---|---|
| `InteractiveScene` | Default (2022+): opens interactive window |
| `Scene` | Simple non-interactive scenes |
| `ThreeDScene` | 3D camera |

```python
from manimlib import *

class MyScene(InteractiveScene):
    def construct(self):
        circle = Circle()
        self.play(ShowCreation(circle))
        self.wait()
```

**Run flags:**
```bash
manimgl scene.py MyScene          # interactive window (default)
manimgl scene.py MyScene -w       # write to file (mp4)
manimgl scene.py MyScene -o       # open output after render
manimgl scene.py MyScene -f       # full quality
manimgl scene.py MyScene -s       # still image (last frame)
manimgl scene.py MyScene -n 10    # start from frame 10
```

---

## Camera: self.frame

In ManimGL the camera is `self.frame`, NOT `self.camera.frame`.

```python
# Zoom in
self.play(self.frame.animate.scale(0.5))

# Pan
self.play(self.frame.animate.shift(RIGHT * 3))

# Zoom out and re-center
self.play(self.frame.animate.scale(2).move_to(ORIGIN))

# Save / restore frame state
self.frame.save_state()
self.play(self.frame.animate.scale(0.3).move_to(some_point))
self.play(Restore(self.frame))
```

**Follow a mobject:**
```python
self.frame.add_updater(lambda f: f.move_to(dot))
self.play(MoveAlongPath(dot, path), run_time=4, rate_func=linear)
self.frame.clear_updaters()
```

---

## Text and math, Tex only

ManimGL has no `MathTex`. All LaTeX goes through `Tex`. Math must be wrapped in `$...$`.

```python
# Math expression
eq = Tex(r"$e^{i\pi} + 1 = 0$")

# Mixed text + math
text = Tex(r"The area is $\pi r^2$.")

# Plain text
label = Text("Hello world", font_size=48)

# Color map (same t2c kwarg)
eq = Tex(r"$\mu_s = n \cdot \mu$", t2c={R"\mu": PINK, "n": YELLOW})
```

Parts are accessed by index, but splitting behavior differs from ManimCE, test indexing carefully:
```python
eq = Tex(r"$a^2 + b^2 = c^2$")
eq[0].set_color(YELLOW)
```

**Avoid:** `OldTex`, `OldTexText`: legacy aliases, do not use in new code.

---

## Animation class differences

| Task | ManimGL | ManimCE equivalent |
|---|---|---|
| Draw outline | `ShowCreation` | `Create` |
| Morph matching LaTeX | `TransformMatchingStrings` | `TransformMatchingTex` |
| Shape morph | `Transform` | `Transform` |
| Fade in | `FadeIn` | `FadeIn` |
| Write text | `Write` | `Write` |

`Create` works in ManimGL as an alias for `ShowCreation` in newer versions, but `ShowCreation` is the canonical name.

---

## time_span: ManimGL exclusive

Specify exactly when within a `self.play()` call each sub-animation fires:

```python
self.play(
    ShowCreation(arrow, time_span=(0.0, 1.0)),
    Write(label, time_span=(0.5, 2.5)),
    FadeIn(box, time_span=(2.0, 3.0)),
    run_time=3,
)
```

`time_span=(start, end)` where values are in seconds within the total `run_time`.
ManimCE has no equivalent, use `Succession` or `lag_ratio` to approximate.

---

## GlowDot and TrueDot, ManimGL exclusive

Preferred point marker style (replaces plain `Dot` in modern 3b1b videos):

```python
# Simple glow dot
dot = GlowDot(point, color=YELLOW)

# Combined solid center + glow (modern 2024+ style)
dot = Group(
    TrueDot(radius=0.05).make_3d(),
    GlowDot(radius=0.15, glow_factor=1.5)
).set_color(YELLOW)
dot.move_to(axes.input_to_graph_point(x, graph))
```

ManimCE equivalent (approximation):
```python
dot_glow = Dot(radius=0.15, color=YELLOW, fill_opacity=0.3)
dot_core = Dot(radius=0.05, color=YELLOW)
dot = VGroup(dot_glow, dot_core)
```

---

## VShowPassingFlash: ManimGL exclusive

Traveling highlight along a path, used for "signal flowing" visuals:

```python
VShowPassingFlash(path, time_width=1, run_time=2)
VShowPassingFlash(arc, time_width=0.3, run_time=1.5)
```

ManimCE has `ShowPassingFlash` with similar behavior.

---

## FlashAround

```python
FlashAround(obj, run_time=2)
FlashAround(obj, time_width=1.5, run_time=2)
```

Similar to `Circumscribe` in ManimCE.

---

## Screen fill utilities

```python
FullScreenRectangle()    # fills entire frame — explicit black background
ScreenRectangle()        # 16:9 inset

# Common pattern
self.add(FullScreenRectangle().set_fill(BLACK, 1))
```

---

## Axes in ManimGL

```python
axes = Axes(x_range=(-4, 4), y_range=(-3, 3))

# Plot — note: get_graph() not plot()
graph = axes.get_graph(lambda x: np.sin(x), color=BLUE)

# Input-to-graph point
point = axes.input_to_graph_point(x_val, graph)

# Get graph label
label = axes.get_graph_label(graph, Tex(r"$\sin(x)$"))
```

Note: ManimCE uses `axes.plot()`, `axes.c2p()`, `axes.get_graph_label(graph, "label")`.
ManimGL uses `axes.get_graph()`, `axes.input_to_graph_point()`.

---

## InteractiveScene features

```python
def construct(self):
    self.play(ShowCreation(circle))
    self.embed()   # drop into ipython — type self.play(...) interactively
```

Press Space to pause/resume the window. Click to select mobjects. Scroll to zoom.

---

## Class attributes (2022+ style)

Use class attributes instead of the old `CONFIG = {}` dict:

```python
class MyScene(InteractiveScene):
    n_bars = 10
    fill_color = BLUE
    animate_boundary = True
```

Old style (pre-2022, avoid in new code):
```python
CONFIG = {"n_bars": 10, "fill_color": BLUE}
```

---

## What ManimGL does NOT have

- `BarChart`: no built-in bar chart
- `Graph` (network graph visualization): no built-in
- `MathTex`: use `Tex` with `$...$`
- `next_section()` / section-based rendering
- `ZoomedScene`: use `self.frame.animate.scale()` instead
- `--save_last_frame`: use `-s` flag

## What ManimCE does NOT have (ManimGL exclusives)

- `GlowDot`, `TrueDot`
- `time_span` in `self.play()`
- `InteractiveScene` with live window
- `self.frame` (ManimCE: `self.camera.frame`)
- `VShowPassingFlash` (CE has `ShowPassingFlash`, different)
- `embed()` for live debugging
- `FullScreenRectangle`, `ScreenRectangle`
