# ManimCE — Animations Deep Reference

**Import:** `from manim import *`

## Animation taxonomy

| Class | What it does |
|---|---|
| `Create` | Draw stroke of VMobject |
| `Uncreate` | Reverse of Create |
| `DrawBorderThenFill` | Outline then fill |
| `Write` | Stroke-by-stroke (good for text) |
| `FadeIn` / `FadeOut` | Opacity transition |
| `GrowFromCenter` | Scale from 0 at center |
| `GrowFromPoint` | Scale from 0 at a point |
| `GrowArrow` | Extend arrow from tail |
| `SpinInFromNothing` | Rotate in from scale 0 |
| `Transform` | Morph a into b (keeps a in scene as b) |
| `ReplacementTransform` | Morph a into b (removes a, adds b) |
| `TransformMatchingTex` | Smart morph matching LaTeX tokens |
| `TransformMatchingShapes` | Smart morph by shape similarity |
| `MoveToTarget` | Move to pre-set `.target` copy |
| `Restore` | Move back to saved state |
| `Indicate` | Scale-pulse highlight |
| `Circumscribe` | Draw box or circle around |
| `Flash` | Burst of lines from a point |
| `ApplyFunction` | Apply arbitrary point transform |
| `Rotate` | Rotate about a point |
| `ScaleInPlace` | Scale without moving center |

---

## .animate syntax

Preferred for simple property changes:

```python
self.play(obj.animate.shift(RIGHT))
self.play(obj.animate.scale(2).set_color(RED).rotate(PI/4))
```

Limitation: `.animate` interpolates start-to-end linearly. For curved paths or value-driven animation, use updaters or `MoveAlongPath`.

---

## ValueTracker

The primary tool for driving continuous animation:

```python
t = ValueTracker(0)

dot = Dot()
dot.add_updater(lambda d: d.move_to(np.array([t.get_value(), np.sin(t.get_value()), 0])))
self.add(dot)
self.play(t.animate.set_value(TAU), run_time=4)
dot.clear_updaters()
```

Multiple trackers:
```python
x_tracker = ValueTracker(0)
y_tracker = ValueTracker(0)
dot = Dot()
dot.add_updater(lambda d: d.move_to(axes.c2p(x_tracker.get_value(), y_tracker.get_value())))
self.play(x_tracker.animate.set_value(3), y_tracker.animate.set_value(2))
```

---

## Updater functions

Two types: dt-updaters (receive elapsed time) and position-updaters (just update):

```python
# Position updater — runs every frame
label.add_updater(lambda l: l.next_to(dot, UP))

# dt updater — receives delta time
clock_hand.add_updater(lambda m, dt: m.rotate(-dt * PI, about_point=ORIGIN))

self.wait(3)
label.clear_updaters()
```

`always_redraw` recreates the mobject every frame — use for complex redraws:
```python
tangent_line = always_redraw(lambda: get_tangent_at(t.get_value()))
```

---

## Custom Animation subclass

```python
class CountUp(Animation):
    def __init__(self, number: DecimalNumber, target: float, **kwargs):
        self.target = target
        super().__init__(number, **kwargs)

    def interpolate_mobject(self, alpha: float):
        value = self.mobject.get_value() + (self.target - self.mobject.get_value()) * alpha
        self.mobject.set_value(value)

counter = DecimalNumber(0, num_decimal_places=0)
self.play(CountUp(counter, 100), run_time=3)
```

---

## MoveAlongPath

```python
path = VMobject()
path.set_points_as_corners([ORIGIN, UP * 2, UP * 2 + RIGHT * 3, RIGHT * 3])

dot = Dot(ORIGIN)
self.play(MoveAlongPath(dot, path), run_time=3, rate_func=linear)
```

---

## ApplyFunction (point-wise transform)

```python
def warp(point):
    x, y, z = point
    return np.array([x + 0.2 * y**2, y, z])

self.play(ApplyFunction(warp, grid))
```

---

## MoveToTarget pattern

Useful when you want to pre-compute an end state:

```python
obj = Square()
obj.generate_target()
obj.target.shift(RIGHT * 3).set_color(BLUE).rotate(PI/4)
self.play(MoveToTarget(obj))
```

---

## Save / Restore

```python
obj = Circle()
self.play(Create(obj))
obj.save_state()

self.play(obj.animate.scale(3).set_color(RED))
self.wait(1)
self.play(Restore(obj))   # back to saved state
```

---

## Succession and LaggedStart

```python
# Run one after another
self.play(Succession(
    Create(a), Create(b), Create(c)
))

# Staggered start (each begins before previous ends)
self.play(LaggedStart(
    FadeIn(a), FadeIn(b), FadeIn(c),
    lag_ratio=0.4,   # 0=simultaneous, 1=fully sequential
    run_time=3
))

# Lagged map over a group
self.play(LaggedStartMap(FadeIn, vgroup, lag_ratio=0.1))
```

---

## AnimationGroup

```python
self.play(AnimationGroup(
    Create(circle),
    Write(label),
    lag_ratio=0,   # simultaneous
))
```

---

## DecimalNumber (live counter)

```python
number = DecimalNumber(0, num_decimal_places=2, font_size=72)
self.add(number)

tracker = ValueTracker(0)
number.add_updater(lambda n: n.set_value(tracker.get_value()))
self.play(tracker.animate.set_value(100), run_time=4, rate_func=linear)
```

---

## Rate functions

```python
from manim import *

# Built-in
linear, smooth, rush_into, rush_from
there_and_back, there_and_back_with_pause
ease_in_sine, ease_out_sine, ease_in_out_sine
ease_in_quad, ease_out_quad, ease_in_out_quad
# ... cubic, quart, quint, expo, circ, back, elastic, bounce

# Custom
def my_rate(t): return t**3
self.play(Create(obj), rate_func=my_rate)
```
