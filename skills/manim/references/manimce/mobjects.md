# ManimCE: Mobjects Deep Reference

**Import:** `from manim import *`

## VMobject internals

All vector mobjects inherit from `VMobject`. Key properties:
- `points`: numpy array of bezier control points
- `submobjects`: list of child VMobjects
- `fill_color`, `stroke_color`, `stroke_width`

```python
class CustomShape(VMobject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_points_as_corners([
            UP, UP + RIGHT, RIGHT, ORIGIN, UP
        ])
```

For smooth curves, use `set_points_smoothly`:
```python
self.set_points_smoothly([ORIGIN, UP, RIGHT, DOWN])
```

---

## NumberLine

```python
nl = NumberLine(
    x_range=[-5, 5, 1],
    length=10,
    include_numbers=True,
    include_tip=True,
    label_direction=DOWN,
)
self.play(Create(nl))

# Add a dot at a value
dot = Dot(nl.n2p(2.5), color=RED)
self.play(FadeIn(dot))
```

---

## Axes and coordinate systems

```python
axes = Axes(
    x_range=[-4, 4, 1],
    y_range=[-3, 3, 1],
    x_length=8,
    y_length=6,
    axis_config={
        "include_tip": True,
        "numbers_to_include": [-2, -1, 1, 2],
    },
)
axes.add_coordinates()

# Convert between math coords and scene coords
point = axes.c2p(2, 1)   # coords-to-point
value = axes.p2c(point)  # point-to-coords
```

**Plotting:**
```python
graph = axes.plot(lambda x: np.sin(x), x_range=[-PI, PI], color=YELLOW)
area = axes.get_area(graph, x_range=[0, PI], color=BLUE, opacity=0.3)
label = axes.get_graph_label(graph, "\\sin(x)", x_val=PI/2, direction=UP)
```

**Parametric curve:**
```python
curve = axes.plot_parametric_curve(
    lambda t: np.array([np.cos(t), np.sin(t)]),
    t_range=[0, TAU],
    color=GREEN
)
```

---

## NumberPlane

```python
plane = NumberPlane(
    x_range=[-5, 5],
    y_range=[-4, 4],
    background_line_style={"stroke_opacity": 0.5}
)
self.add(plane)
```

---

## VGroup and arrangement

```python
dots = VGroup(*[Dot() for _ in range(5)])
dots.arrange(RIGHT, buff=0.3)

# Grid arrangement
grid = VGroup(*[Square(side_length=0.5) for _ in range(9)])
grid.arrange_in_grid(rows=3, cols=3, buff=0.1)
```

---

## Always-redraw updaters

Use `always_redraw` to create a mobject that redraws every frame based on current state:

```python
tracker = ValueTracker(0)

dot = always_redraw(lambda: Dot(
    axes.c2p(tracker.get_value(), np.sin(tracker.get_value())),
    color=RED
))

tangent = always_redraw(lambda: axes.get_tangent_line(
    x=tracker.get_value(),
    graph=graph,
    length=2,
    color=YELLOW
))

self.add(dot, tangent)
self.play(tracker.animate.set_value(TAU), run_time=5)
```

---

## Table

```python
table = Table(
    [["1", "2", "3"],
     ["4", "5", "6"],
     ["7", "8", "9"]],
    row_labels=[Text("R1"), Text("R2"), Text("R3")],
    col_labels=[Text("C1"), Text("C2"), Text("C3")],
    include_outer_lines=True,
)
self.play(table.create())
self.play(table.get_highlighted_cell((2, 2), color=YELLOW).animate.set_opacity(1))
```

---

## MathTex internals

`MathTex` splits on `&` and `\\` by default. Access individual parts:

```python
eq = MathTex(r"e", r"^{i\pi}", r"+ 1 = 0")
# eq[0] = "e", eq[1] = "^{i\pi}", eq[2] = "+ 1 = 0"
eq[1].set_color(YELLOW)
```

For `TransformMatchingTex` to work, matching substrings must be separate arguments:
```python
eq1 = MathTex(r"x^2", r"+", r"2x", r"+", r"1")
eq2 = MathTex(r"(", r"x", r"+", r"1", r")^2")
self.play(TransformMatchingTex(eq1, eq2))
```

---

## SVGMobject and ImageMobject

```python
svg = SVGMobject("path/to/file.svg")
svg.scale(2).set_color(BLUE)
self.play(Create(svg))

img = ImageMobject("path/to/image.png")
img.scale(3)
self.add(img)
```

---

## Brace and annotation

```python
brace = Brace(some_mobject, direction=DOWN)
label = brace.get_text("label")
self.play(GrowFromCenter(brace), Write(label))
```

---

## Useful utility methods

```python
obj.get_center()          # numpy array
obj.get_top()             # top edge center
obj.get_bottom()
obj.get_left()
obj.get_right()
obj.get_width()
obj.get_height()
obj.copy()                # deep copy — important before Transform
obj.surround(other)       # resize to surround another object
SurroundingRectangle(obj, color=YELLOW, buff=0.1)
Underline(text_obj)
Cross(obj)                # X mark through object
```
