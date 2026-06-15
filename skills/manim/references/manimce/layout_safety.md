# ManimCE — Layout Safety: Overlap and Boundary Checks

**Import:** `from manim import *`

Elements that overlap or escape the frame are the most common way Manim animations look broken.
Apply ALL checks in this file before calling self.play() on any new element.

---

## Frame boundaries

The visible frame is exactly:
- Width: 14.22 units — x must stay within [-7.11, 7.11]
- Height: 8.0 units — y must stay within [-4.0, 4.0]

```python
FRAME_X_LIMIT = 7.0    # leave 0.11 margin
FRAME_Y_LIMIT = 3.8    # leave 0.2 margin
```

**Check every mobject is inside the frame before adding it:**

```python
def check_in_frame(mob, name="mob"):
    bbox = mob.get_bounding_box()   # [left-bottom, center, right-top]
    l, b = bbox[0][0], bbox[0][1]
    r, t = bbox[2][0], bbox[2][1]
    issues = []
    if l < -FRAME_X_LIMIT: issues.append(f"left edge {l:.2f} < -{FRAME_X_LIMIT}")
    if r >  FRAME_X_LIMIT: issues.append(f"right edge {r:.2f} > {FRAME_X_LIMIT}")
    if b < -FRAME_Y_LIMIT: issues.append(f"bottom edge {b:.2f} < -{FRAME_Y_LIMIT}")
    if t >  FRAME_Y_LIMIT: issues.append(f"top edge {t:.2f} > {FRAME_Y_LIMIT}")
    if issues:
        print(f"[LAYOUT WARNING] '{name}' out of frame: {', '.join(issues)}")
    return len(issues) == 0
```

---

## Overlap detection between two mobjects

```python
def overlaps(a, b, margin=0.15):
    """Return True if mobjects a and b overlap (with margin as breathing room).

    margin=0.15  — default for text/equations; anything closer looks cramped
    margin=0.05  — tight mode for bars, grid tiles, or intentionally adjacent shapes
    margin=0.0   — exact bounding-box intersection only
    """
    x_ok = a.get_left()[0]   < b.get_right()[0]  + margin and \
           a.get_right()[0]  > b.get_left()[0]   - margin
    y_ok = a.get_bottom()[1] < b.get_top()[1]    + margin and \
           a.get_top()[1]    > b.get_bottom()[1] - margin
    return x_ok and y_ok
```

**Check all pairs in a group:**

```python
def check_no_overlaps(mobs, names=None, margin=0.15, raise_on_fail=False):
    """Warn on every overlapping pair in a list of mobjects.

    Set raise_on_fail=True in test/CI contexts to hard-stop on layout bugs.
    """
    names = names or [f"mob_{i}" for i in range(len(mobs))]
    ok = True
    for i in range(len(mobs)):
        for j in range(i + 1, len(mobs)):
            if overlaps(mobs[i], mobs[j], margin):
                msg = f"[LAYOUT WARNING] '{names[i]}' overlaps '{names[j]}'"
                if raise_on_fail:
                    raise AssertionError(msg)
                print(msg)
                ok = False
    return ok
```

---

## Standard usage pattern

Add these helpers at the top of your scene file (outside the class), then call them throughout `construct()`:

```python
from manim import *

FRAME_X_LIMIT = 7.0
FRAME_Y_LIMIT = 3.8

def check_in_frame(mob, name="mob"):
    l = mob.get_left()[0];  r = mob.get_right()[0]
    b = mob.get_bottom()[1]; t = mob.get_top()[1]
    issues = []
    if l < -FRAME_X_LIMIT: issues.append(f"left {l:.2f}")
    if r >  FRAME_X_LIMIT: issues.append(f"right {r:.2f}")
    if b < -FRAME_Y_LIMIT: issues.append(f"bottom {b:.2f}")
    if t >  FRAME_Y_LIMIT: issues.append(f"top {t:.2f}")
    if issues:
        print(f"[LAYOUT WARNING] '{name}' out of frame: {issues}")
    return not issues

def overlaps(a, b, margin=0.15):
    x_ok = a.get_left()[0]   < b.get_right()[0]  + margin and \
           a.get_right()[0]  > b.get_left()[0]   - margin
    y_ok = a.get_bottom()[1] < b.get_top()[1]    + margin and \
           a.get_top()[1]    > b.get_bottom()[1] - margin
    return x_ok and y_ok

def check_no_overlaps(mobs, names=None, margin=0.15, raise_on_fail=False):
    names = names or [f"mob_{i}" for i in range(len(mobs))]
    ok = True
    for i in range(len(mobs)):
        for j in range(i + 1, len(mobs)):
            if overlaps(mobs[i], mobs[j], margin):
                msg = f"[LAYOUT WARNING] '{names[i]}' overlaps '{names[j]}'"
                if raise_on_fail:
                    raise AssertionError(msg)
                print(msg)
                ok = False
    return ok


class MyScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        title  = Text("My Title", font_size=48).to_edge(UP, buff=0.4)
        label  = Text("A label",  font_size=32).next_to(title, DOWN, buff=0.5)
        axes   = Axes(x_range=[-3, 3], y_range=[-2, 2]).to_edge(DOWN, buff=0.8)

        # Check layout before animating
        check_in_frame(title,  "title")
        check_in_frame(label,  "label")
        check_in_frame(axes,   "axes")
        check_no_overlaps([title, label, axes], ["title", "label", "axes"])

        self.add(axes)
        self.play(Write(title))
        self.play(Write(label))
```

---

## Temporal overlap checking

`check_no_overlaps` only makes sense for elements that are **simultaneously visible**. Track the visible set and check against it when adding or removing elements:

```python
class MyScene(Scene):
    def construct(self):
        self._visible: dict[str, Mobject] = {}

    def show(self, mob, name, animation=FadeIn, **kwargs):
        check_in_frame(mob, name)
        check_no_overlaps(
            list(self._visible.values()) + [mob],
            list(self._visible.keys())   + [name],
        )
        self._visible[name] = mob
        self.play(animation(mob), **kwargs)

    def hide(self, name, animation=FadeOut, **kwargs):
        mob = self._visible.pop(name, None)
        if mob:
            self.play(animation(mob), **kwargs)
```

Usage:
```python
self.show(title, "title", Write)
self.show(axes,  "axes",  Create)
self.hide("title")          # removes from visible set before adding step label
self.show(step_label, "step_label", Write)
```

This prevents false positives from elements that never co-exist on screen.

---

## Label-over-curve overlap check

Graph labels sitting on top of a colored curve are a silent visual bug — the bounding boxes often don't overlap but the label still reads poorly. Two mitigations:

```python
# 1. Always set backstroke for any label near a graph
label.set_backstroke(BLACK, width=5)

# 2. After placing the label, verify it doesn't intersect the curve's bounding box
def check_label_clear_of_curve(label, curve, name="label", margin=0.15):
    if overlaps(label, curve, margin=margin):
        print(f"[LAYOUT WARNING] '{name}' sits over the curve — reposition or increase buff")
        return False
    return True
```

```python
graph_label = axes.get_graph_label(graph, r"f(x)", x_val=2.5, direction=UP)
graph_label.set_backstroke(BLACK, width=5)
check_label_clear_of_curve(graph_label, graph, "graph_label")
```

If the check fires, move the label along the curve's proportion:
```python
graph_label.move_to(graph.point_from_proportion(0.85) + UP * 0.4)
```

---

## Common overlap causes and fixes

### 1. Title + equation stack too tall

**Problem:** `title.to_edge(UP)` + several stacked equations push the bottom element off-screen.

**Fix:** Reduce spacing or scale down:
```python
stack = VGroup(title, eq1, eq2, eq3)
stack.arrange(DOWN, buff=0.35)
stack.to_edge(UP, buff=0.4)
check_in_frame(stack, "equation_stack")
```

### 2. Axes labels collide with title

**Problem:** Axes positioned at center while title hangs down into the plot area.

**Fix:** Reserve the top area, shift axes down:
```python
title.to_edge(UP, buff=0.3)
title_bottom = title.get_bottom()[1]
axes.shift(DOWN * max(0, title_bottom - axes.get_top()[1] + 0.3))
check_in_frame(axes, "axes")
check_no_overlaps([title, axes], ["title", "axes"])
```

### 3. Side labels collide with axis numbers

**Problem:** A label placed with `next_to(graph, RIGHT)` runs off the right edge.

**Fix:** Clamp to frame and check:
```python
label.next_to(graph.point_from_proportion(0.7), UR, buff=0.1)
if label.get_right()[0] > FRAME_X_LIMIT:
    label.to_edge(RIGHT, buff=0.3)
check_in_frame(label, "graph_label")
```

### 4. LaggedStart group members pile up

**Problem:** A `VGroup` arranged left-to-right is wider than the frame.

**Fix:** Check width before arranging:
```python
group.arrange(RIGHT, buff=0.3)
if group.get_width() > 2 * FRAME_X_LIMIT - 0.5:
    group.set_width(2 * FRAME_X_LIMIT - 0.5)
check_in_frame(group, "group")
```

### 5. Long equations overflow horizontally

**Problem:** A `MathTex` with a long formula is wider than the frame.

**Fix:** Always cap equation width:
```python
eq = MathTex(r"\text{very long formula...}")
eq.set_width(min(eq.get_width(), 12.0))
check_in_frame(eq, "equation")
```

### 6. Annotation obscures the main visual

**Problem:** `next_to(axes, RIGHT)` puts text on top of the graph when the graph is wide.

**Fix:** Use corner positioning and explicitly check:
```python
annotation.to_corner(UR, buff=0.3)
check_no_overlaps([axes, annotation], ["axes", "annotation"])
```

---

## Layout budget — plan before coding

Before writing a scene, sketch the vertical budget:
```
FRAME_HEIGHT = 8.0 units

TOP MARGIN   0.4
TITLE        ~0.7  (font_size=48)
GAP          0.4
SUBTITLE     ~0.5  (font_size=36)
GAP          0.4
MAIN VISUAL  ?     <- remaining space
GAP          0.3
BOTTOM       0.4
─────────────────
Budget for main visual = 8.0 - 0.4 - 0.7 - 0.4 - 0.5 - 0.4 - 0.3 - 0.4 = 4.9 units
```

For a typical title + graph scene:
- Title at top: 0.4 buff — occupies roughly y in [3.0, 3.8]
- Axes: set `height=4.5` max — fits below title

---

## get_bounding_box() reference

`mob.get_bounding_box()` returns a `(3, 3)` numpy array:
```
bbox[0] = left-bottom corner  [x_min, y_min, 0]
bbox[1] = center              [x_mid, y_mid, 0]
bbox[2] = right-top corner    [x_max, y_max, 0]
```

Equivalent helpers:
```python
mob.get_left()      # = [x_min, y_mid, 0]
mob.get_right()     # = [x_max, y_mid, 0]
mob.get_top()       # = [x_mid, y_max, 0]
mob.get_bottom()    # = [x_mid, y_min, 0]
mob.get_width()     # = x_max - x_min
mob.get_height()    # = y_max - y_min
mob.get_center()    # = [x_mid, y_mid, 0]
```

---

## Checklist — run before every render

- [ ] Every mobject passes `check_in_frame()`
- [ ] All **simultaneously visible** elements pass `check_no_overlaps()` — not just all elements in the file
- [ ] No equation wider than 12 units
- [ ] Axes height <= 4.5 if title present, <= 6 if no title
- [ ] Labels on graphs have `set_backstroke(BLACK, 5)` and pass `check_label_clear_of_curve()`
- [ ] Groups wider than frame scaled down with `group.set_width(max_w)`
- [ ] `next_to()` calls use appropriate buff (min `SMALL_BUFF = 0.1`)
- [ ] Sidebar items placed by slot constant, not raw coordinate
- [ ] `check_no_overlaps` margin is `0.15` for text/equations, `0.05` only for bars/tiles
