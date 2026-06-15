# Design Principles — 3b1b Visual Style

Extracted from reading Python files across every year (_2015-_2026) and the `custom/` folder of github.com/3b1b/videos.

3b1b uses ManimGL. Patterns below apply to ManimCE unless explicitly marked **[GL only]**.
ManimCE-specific equivalents are noted inline where the API differs.

---

## 1. Background and base palette

Always BLACK background. Never white or grey.

```python
# ManimCE
config.background_color = BLACK
```

ManimGL also uses `FullScreenRectangle()` for an explicit black background **[GL only]**:
```python
self.add(FullScreenRectangle())
```

---

## 2. Color system

### 2.1 The grey hierarchy — text and secondary elements

Grey constants go from lightest to darkest:
- `GREY_A` — near-white; secondary text, de-emphasized annotations
- `GREY_B` — muted labels, axis separators, structural arrows
- `GREY_C` — subtle grid lines (often at 0.5-0.75 stroke opacity)
- `GREY_D` — background fills for diagram panels
- `GREY_E` — near-black fills; dark background rectangles
- `GREY_BROWN` — Mortimer pi creature, earthy secondary elements

**Rule:** Annotation text that shouldn't compete with math uses `GREY_A` or `GREY_B`, not WHITE.

### 2.2 Concept-to-color mapping (the most important design rule)

Pick one color per concept and never break it within a video:

| Concept | Color |
|---|---|
| Primary variable / position | `BLUE` / `BLUE_D` |
| Time variable `t` | `BLUE` |
| Laplace variable `s` | `YELLOW` |
| Velocity / first derivative | `RED` |
| Second derivative | `YELLOW` |
| Mean `mu` | `PINK` or `BLUE_B` |
| Standard deviation `sigma` | `RED` |
| Eigenvalues | `TEAL_A`, `TEAL_D` |
| Graph function 1 | `BLUE` |
| Graph function 2 | `YELLOW` or `RED` |
| Result / output | `TEAL` or `GREEN` |
| Prime numbers | `YELLOW` |
| Key highlight | `YELLOW` |
| Author name in quote | `YELLOW` |

### 2.3 The t2c pattern — mandatory for equations

`t2c` (tex_to_color_map) is the dominant design tool. Define it once, reuse across every equation in the scene:

```python
# ManimCE
COLOR_MAP = {
    R"\mu": PINK,
    R"\sigma": RED,
    "n": YELLOW,
}
eq1 = MathTex(r"\mu_s = n \cdot \mu", t2c=COLOR_MAP)
eq2 = MathTex(r"\sigma_s = \sqrt{n} \cdot \sigma", t2c=COLOR_MAP)
```

```python
# ManimGL — same kwarg, but Tex not MathTex, and math needs $...$
eq1 = Tex(r"$\mu_s = n \cdot \mu$", t2c=COLOR_MAP)
```

### 2.4 Shades within a color family

Use dark-to-light shade variants for depth:
- `BLUE_E` (darkest) — fill backgrounds, bar darks
- `BLUE_D` — primary shape fill color
- `BLUE_C` — secondary emphasis
- `BLUE_B` — bright highlight
- `BLUE_A` (lightest) — rare, very subtle

Same pattern applies to `TEAL_*`, `GREEN_*`, `RED_*`, `GREY_*`.

### 2.5 Gradient coloring for sequences

```python
bars.set_submobject_colors_by_gradient(BLUE_D, TEAL)
bars.set_color_by_gradient(BLUE_D, GREEN_D)
```

### 2.6 Value-to-color for signed quantities (2024+)

Standard pattern for weight matrices / activations:
```python
def value_to_color(value,
    low_positive_color=BLUE_E, high_positive_color=BLUE_B,
    low_negative_color=RED_E,  high_negative_color=RED_B,
    min_value=0.0, max_value=10.0):
    alpha = clip(float(inverse_interpolate(min_value, max_value, abs(value))), 0, 1)
    colors = (low_positive_color, high_positive_color) if value >= 0 else (low_negative_color, high_negative_color)
    return interpolate_color_by_hsl(*colors, alpha)
```

Positive = blue family. Negative = red family. Magnitude = brightness.

---

## 3. Typography

### 3.1 Text class selection

| Situation | ManimCE | ManimGL |
|---|---|---|
| Prose / labels / UI text | `Text` | `Text` |
| Mathematical expressions | `MathTex` | `Tex` with `$...$` |
| Mixed text + math | `Tex` with `\text{}` | `Tex` |
| Live-updating number | `DecimalNumber` | `DecimalNumber` |

Do NOT use `OldTex` or `OldTexText` — legacy ManimGL classes from pre-2022.

### 3.2 Font sizes — exact values

| Context | font_size |
|---|---|
| Section title, chapter | 72 |
| Sub-heading | 60 |
| Main equation / primary body | 48 |
| Standard body / derivation steps | 36 |
| Annotation, axis labels | 24-30 |
| Axis tick numbers | 20-24 |
| Dense multi-formula layouts | 30-36 |

Always pass `font_size` explicitly — never rely on defaults.

### 3.3 Text alignment

```python
Text("...", alignment="LEFT")
equations.arrange(DOWN, aligned_edge=LEFT)   # left-flush equation stacks
```

### 3.4 Backstroke for legibility

Whenever text sits on top of a colored graph, surface, or filled shape:
```python
label.set_backstroke(BLACK, width=5)
label.set_backstroke()
label.set_backstroke(width=3)
```

Used universally on graph labels from 2022+.

---

## 4. Timing and pacing

### 4.1 run_time by animation type

| Animation | Typical run_time |
|---|---|
| `Write` (short label) | 1.0 |
| `Write` (paragraph) | 2.0-3.0 |
| `FadeIn` / `FadeOut` (single) | 0.5-1.0 |
| `Create` (simple) | 1.0-2.0 |
| `Create` (graph/curve) | 2.0-3.0 |
| `LaggedStartMap` (many items) | 2.0-4.0 |
| `Transform` / `ReplacementTransform` | 1.0-1.5 |
| `TransformMatchingTex` | 1.0-2.0 |
| `GrowArrow` / `GrowFromCenter` | 1.0 |
| Camera reorient / frame move | 2.0-8.0 |

### 4.2 wait() durations

```python
self.wait()     # 1 second — after every significant animation beat
self.wait(2)    # after major reveals or idea transitions
self.wait(3)    # after complex ideas that need processing time
self.wait(0.5)  # brief pause mid-sequence
self.wait(0.25) # micro-pause between rapid items
```

**Rule:** `self.wait()` follows essentially every `.play()` call that reveals something new.

### 4.3 lag_ratio values

| Context | lag_ratio |
|---|---|
| Nearly simultaneous | 0.01-0.02 |
| Fast cascade (many small items) | 0.025-0.05 |
| Standard group fade-in | 0.1-0.15 |
| A few key items | 0.25-0.3 |
| Few large dramatic items | 0.4-0.5 |
| Fully sequential | 1.0 |

### 4.4 Rate functions

| Situation | rate_func |
|---|---|
| Default for most animations | `smooth` (implicit) |
| Graph traversal, count-up numbers | `linear` |
| Rapid pop-in | `rush_into` |
| Bounce / overshoot | `overshoot` |
| Flash then return | `there_and_back` |

---

## 5. Layout and positioning

### 5.1 Frame dimensions

```
FRAME_WIDTH  = 14.22 units
FRAME_HEIGHT = 8.0 units
```

### 5.2 buff constants

| Constant | Value | Use |
|---|---|---|
| `SMALL_BUFF` | 0.1 | Tight: brace-to-formula, SurroundingRectangle |
| `MED_SMALL_BUFF` | 0.25 | Normal `next_to` spacing |
| `MED_LARGE_BUFF` | 0.5 | Breathing room between related groups |
| `LARGE_BUFF` | 1.0 | Separation between distinct sections |
| `0` | 0.0 | Touching elements: bars, grid tiles |

### 5.3 Named screen zones

Define these at the top of every scene file so placement is never a magic number:

```python
# Zone boundaries (all in Manim coordinate units)
TITLE_Y_TOP    =  3.8   # to_edge(UP, buff=0.3) lands here
TITLE_Y_BOT    =  2.9   # bottom of a font_size=48 title
FOOTER_Y       = -3.3   # to_edge(DOWN, buff=0.5)

# Full-frame main visual (no title, no sidebar)
MAIN_X_CENTER  =  0.0
MAIN_Y_CENTER  =  0.0

# Split-screen: left panel (graph/diagram) + right sidebar (equations/annotations)
LEFT_PANEL_CENTER  = LEFT  * 1.8          # move_to for axes
RIGHT_PANEL_X      =  4.35                # x anchor for sidebar items
SIDEBAR_SLOT_TOP   =  1.8                 # slot 0 — primary equation
SIDEBAR_SLOT_1     =  1.0                 # slot 1
SIDEBAR_SLOT_2     =  0.2                 # slot 2
SIDEBAR_SLOT_3     = -0.6                 # slot 3
SIDEBAR_SLOT_BOT   = -1.4                 # slot 4 — lowest annotation
```

Use slots instead of raw coordinates:
```python
formula.move_to(RIGHT * RIGHT_PANEL_X + UP * SIDEBAR_SLOT_TOP)
note.move_to(RIGHT   * RIGHT_PANEL_X + UP * SIDEBAR_SLOT_2)
```

### 5.4 Standard positioning idioms

```python
mob.to_edge(UP, buff=MED_SMALL_BUFF)        # title placement
mob.to_corner(UL)                            # equation stack
mob.to_corner(DR)                            # legend / secondary info
mob.to_edge(DOWN, buff=LARGE_BUFF)           # axes base
mob.center()                                 # standalone main visual

equations.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
group.arrange(RIGHT, buff=MED_LARGE_BUFF)
touching_bars.arrange(RIGHT, buff=0)
grid.arrange_in_grid(n_cols=4, aligned_edge=LEFT)
```

### 5.5 Split-screen layout pattern

The most common multi-element layout: graph on the left, annotations stacked on the right.

```python
# Axes occupy the left ~60 % of the frame
axes = Axes(...).move_to(LEFT_PANEL_CENTER + DOWN * 0.2)

# Sidebar items are anchored to RIGHT_PANEL_X and stacked by slot
primary_eq  = MathTex(...).move_to(RIGHT * RIGHT_PANEL_X + UP * SIDEBAR_SLOT_TOP)
secondary   = Text(...).move_to(RIGHT   * RIGHT_PANEL_X + UP * SIDEBAR_SLOT_2)
footer_note = Text(...).move_to(RIGHT   * RIGHT_PANEL_X + UP * SIDEBAR_SLOT_BOT)

# Safety checks before any self.play()
check_in_frame(axes,        "axes")
check_in_frame(primary_eq,  "primary_eq")
check_in_frame(secondary,   "secondary")
check_no_overlaps([axes, primary_eq, secondary], ["axes", "primary_eq", "secondary"])
```

When replacing a sidebar item, fade out the old one before placing the new one at the same slot so the frame never holds two items at the same position.

---

## 6. Animation class selection

### 6.1 Creation

| Situation | ManimCE | ManimGL |
|---|---|---|
| Graph curves, VMobject outlines | `Create` | `ShowCreation` |
| Filled shapes | `DrawBorderThenFill` | `DrawBorderThenFill` |
| Mathematical text | `Write` | `Write` |
| Directional arrows | `GrowArrow` | `GrowArrow` |
| Simple fade in | `FadeIn` | `FadeIn` |
| Copy flies to destination | `TransformFromCopy` | `TransformFromCopy` |

### 6.2 Transform

| Situation | ManimCE | ManimGL |
|---|---|---|
| Matching LaTeX tokens morph | `TransformMatchingTex` | `TransformMatchingStrings` |
| Shape morphs | `Transform` / `ReplacementTransform` | same |
| Dissolve between shapes | `FadeTransform` | `FadeTransform` |

### 6.3 time_span — ManimGL only **[GL only]**

```python
# ManimGL only:
self.play(
    FadeIn(arrow, time_span=(0.7, 1.0)),
    Write(bubble, time_span=(0.0, 2.0)),
    run_time=3,
)
```

ManimCE equivalent: use `Succession` or `lag_ratio`.

### 6.4 Removal

```python
self.play(FadeOut(mob))
self.play(FadeOut(mob, UP))
self.play(FadeOut(group, lag_ratio=0.1))
mob.animate.set_opacity(0)    # fade without removing from scene
```

---

## 7. Emphasis and attention

### 7.1 Hierarchy (lightest to heaviest)

1. `obj.animate.set_color(YELLOW)` — color shift
2. `Indicate(obj)` — brief scale pulse
3. `WiggleOutThenIn(obj)` — wobble
4. `FlashAround(obj)` — ring of lines **[GL: FlashAround, CE: Circumscribe]**
5. `Flash(point)` — star burst
6. `SurroundingRectangle`:
   ```python
   box = SurroundingRectangle(obj, color=YELLOW, buff=SMALL_BUFF)
   box.round_corners(radius=0.1)   # modern 2022+ style
   ```

Use at most two emphasis techniques in one scene.

### 7.2 VShowPassingFlash — traveling highlight **[GL only]**

```python
VShowPassingFlash(path, time_width=1, run_time=2)
```

ManimCE has `ShowPassingFlash` with similar but different behavior.

### 7.3 GlowDot — modern point marker **[GL only]**

```python
dot = GlowDot(point, color=YELLOW)
```

ManimCE equivalent (approximation):
```python
dot_glow = Dot(radius=0.15, color=YELLOW, fill_opacity=0.3)
dot_core = Dot(radius=0.05, color=YELLOW)
dot = VGroup(dot_glow, dot_core)
```

### 7.4 De-emphasis over removal

When an element loses focus, fade rather than remove:
```python
self.play(old_eq.animate.scale(0.75, about_edge=UR).set_opacity(0.5))
self.play(background_group.animate.set_opacity(0.4))
```

---

## 8. Fills and strokes

| Object | stroke_width |
|---|---|
| Main graph curve | 3 |
| Axis lines | 1-2 |
| SurroundingRectangle | 2 |
| Vectors / arrows | 3-5 |

| Object | fill_opacity |
|---|---|
| Solid background panel | 1.0 |
| Bar chart bars | 0.5 |
| Shaded area under graph | 0.5-0.75 |
| SurroundingRectangle highlight fill | 0.15-0.2 |
| Ghost / reference copy | 0.0-0.3 |

---

## 9. Scene structure

### 9.1 Scene class

| | ManimCE | ManimGL |
|---|---|---|
| Default | `Scene` | `InteractiveScene` (2022+) |
| Camera animation | `MovingCameraScene` | Camera is `self.frame` on any scene |
| 3D | `ThreeDScene` | `ThreeDScene` |

### 9.2 construct() structure

```python
def construct(self):
    # 1. Setup — create objects, no animation
    axes = Axes(...)
    graph = axes.plot(func, color=BLUE)   # ManimCE
    # graph = axes.get_graph(func, color=BLUE)   # ManimGL

    # 2. First beat — background goes in with self.add(), content with self.play()
    self.add(axes)
    self.play(Create(graph))   # ManimCE: Create, ManimGL: ShowCreation
    self.wait()

    # 3. Label
    label = MathTex(r"f(x) = x^2")  # ManimCE — use Tex in ManimGL
    self.play(Write(label))
    self.wait()

    # 4. Emphasis
    self.play(Circumscribe(graph))   # ManimCE — use FlashAround in ManimGL
    self.wait()

    # 5. Transform
    self.play(TransformMatchingTex(eq1, eq2))  # ManimCE — TransformMatchingStrings in GL
    self.wait(2)
```

### 9.3 Class attributes (2022+ style)

```python
class MyScene(Scene):
    n_bars = 10
    fill_color = BLUE
```

Old style (pre-2022, avoid): `CONFIG = {"n_bars": 10}`.

---

## 10. Equation design

### 10.1 Multi-step derivation

```python
# ManimCE
steps = [
    MathTex(r"ax^2 + bx + c = 0", t2c=COLOR_MAP),
    MathTex(r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}", t2c=COLOR_MAP),
]
current = steps[0]
self.play(Write(current))
for next_eq in steps[1:]:
    self.play(TransformMatchingTex(current, next_eq))
    self.wait()
    current = next_eq
```

### 10.2 TransformMatchingTex / TransformMatchingStrings

```python
# ManimCE
self.play(TransformMatchingTex(
    eq1, eq2,
    matched_keys=[R"F(s)", R"e^{st}"],
    path_arc=-0.1 * PI,
    lag_ratio=1e-2,
))

# ManimGL — uses TransformMatchingStrings
self.play(TransformMatchingStrings(eq1, eq2))
```

---

## 11. Axes and graphs

```python
# ManimCE
axes = Axes(x_range=[-4, 4], y_range=[-2, 4])
graph = axes.plot(lambda x: x**2, color=BLUE)
point = axes.c2p(2, 4)   # coords to point
label = axes.get_graph_label(graph, "x^2")
```

```python
# ManimGL
axes = Axes(x_range=(-4, 4), y_range=(-2, 4))
graph = axes.get_graph(lambda x: x**2, color=BLUE)
point = axes.input_to_graph_point(2, graph)
label = axes.get_graph_label(graph, Tex(r"$x^2$"))
```

Graph labels always get `set_backstroke(BLACK, width=5)` when over colored curves.

---

## 12. Quick reference — exact numbers

| Parameter | Value |
|---|---|
| Frame width | 14.22 |
| Frame height | 8.0 |
| Standard wait | 1.0 s |
| Graph stroke_width | 3 |
| SurroundingRectangle stroke_width | 2 |
| SurroundingRectangle buff | `SMALL_BUFF` (0.1) |
| round_corners radius (modern) | 0.1 |
| Bar fill_opacity | 0.5 |
| Shaded area fill_opacity | 0.5-0.75 |
| De-emphasized opacity | 0.4-0.5 |
| LaggedStartMap rapid cascade | lag_ratio 0.025-0.05 |
| LaggedStartMap standard | lag_ratio 0.1-0.25 |
| Pi creature height | 1.25 |
| Opening quote run_time | 5.0 |
| Author name color | YELLOW |
