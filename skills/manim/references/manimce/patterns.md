# ManimCE — Complete Working Examples

All examples use ManimCE (`from manim import *`).

All examples include the layout safety helpers. Copy this block once at the top of every scene file:

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

def check_no_overlaps(mobs, names=None, margin=0.15):
    names = names or [f"mob_{i}" for i in range(len(mobs))]
    for i in range(len(mobs)):
        for j in range(i + 1, len(mobs)):
            if overlaps(mobs[i], mobs[j], margin):
                print(f"[LAYOUT WARNING] '{names[i]}' overlaps '{names[j]}'")
```

---

## 1. Mathematical proof animation (Pythagorean theorem)

```python
from manim import *

class PythagoreanProof(Scene):
    def construct(self):
        a, b = 3, 4
        triangle = Polygon(ORIGIN, RIGHT * a, RIGHT * a + UP * b, color=WHITE)
        check_in_frame(triangle, "triangle")
        self.play(Create(triangle))

        label_a = MathTex("a").next_to(triangle, DOWN)
        label_b = MathTex("b").next_to(triangle, RIGHT)
        label_c = MathTex("c").next_to(triangle.get_center(), UL)
        check_no_overlaps([triangle, label_a, label_b, label_c],
                          ["triangle", "label_a", "label_b", "label_c"])
        self.play(Write(label_a), Write(label_b), Write(label_c))
        self.wait()

        eq = MathTex(r"a^2 + b^2 = c^2").to_edge(UP)
        check_in_frame(eq, "eq")
        self.play(Write(eq))
        self.wait()

        eq2 = MathTex(rf"{a}^2 + {b}^2 = c^2").to_edge(UP)
        eq3 = MathTex(rf"{a**2} + {b**2} = c^2").to_edge(UP)
        eq4 = MathTex(rf"{a**2 + b**2} = c^2").to_edge(UP)
        eq5 = MathTex(rf"c = \sqrt{{{a**2 + b**2}}} = {(a**2+b**2)**0.5:.0f}").to_edge(UP)

        for next_eq in [eq2, eq3, eq4, eq5]:
            self.play(TransformMatchingTex(eq, next_eq))
            eq = next_eq
            self.wait(0.5)

        self.wait(2)
```

---

## 2. Function graph walkthrough

```python
from manim import *

class FunctionExplorer(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 8, 1],
            x_length=10,
            y_length=6,
            axis_config={"include_tip": True, "numbers_to_include": [-3,-2,-1,1,2,3]},
        ).add_coordinates()

        check_in_frame(axes, "axes")
        self.play(Create(axes), run_time=1.5)

        graph = axes.plot(lambda x: x**2, color=YELLOW, x_range=[-2.8, 2.8])
        graph_label = axes.get_graph_label(graph, r"f(x) = x^2", x_val=2.5, direction=UP)
        graph_label.set_backstroke(BLACK, width=5)
        check_in_frame(graph_label, "graph_label")
        self.play(Create(graph), Write(graph_label))
        self.wait()

        t = ValueTracker(-2.5)
        dot = always_redraw(lambda: Dot(axes.c2p(t.get_value(), t.get_value()**2), color=RED))
        x_line = always_redraw(lambda: axes.get_vertical_line(axes.c2p(t.get_value(), t.get_value()**2), color=RED, stroke_width=2))
        coords = always_redraw(lambda: MathTex(
            rf"({t.get_value():.1f},\ {t.get_value()**2:.1f})",
            font_size=32, color=RED
        ).next_to(dot, UR, buff=0.1))

        self.play(FadeIn(dot), Create(x_line), Write(coords))
        self.play(t.animate.set_value(2.5), run_time=5, rate_func=smooth)
        self.wait(2)

        deriv_graph = axes.plot(lambda x: 2*x, color=GREEN, x_range=[-3.5, 3.5])
        deriv_label = axes.get_graph_label(deriv_graph, r"f'(x) = 2x", x_val=3, direction=RIGHT)
        self.play(Create(deriv_graph), Write(deriv_label))
        self.wait(2)
```

---

## 3. 3D surface visualization

```python
from manim import *

class SaddleSurface(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-60 * DEGREES)

        axes = ThreeDAxes(x_range=[-2, 2], y_range=[-2, 2], z_range=[-2, 2])

        surface = Surface(
            lambda u, v: axes.c2p(u, v, u**2 - v**2),
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            resolution=(20, 20),
            fill_opacity=0.85,
        )
        surface.set_fill_by_value(
            axes=axes,
            colorscale=[(BLUE, -2), (GREEN, 0), (RED, 2)],
            axis=2
        )

        title = Text("z = x² - y²  (saddle point)", font_size=36).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        check_in_frame(title, "title")
        self.play(Write(title))
        self.play(Create(axes), Create(surface), run_time=3)
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(6)
        self.stop_ambient_camera_rotation()
```

---

## 4. Data bar chart animation

```python
from manim import *

class BarChartAnimation(Scene):
    def construct(self):
        data = {"Mon": 4, "Tue": 7, "Wed": 3, "Thu": 9, "Fri": 6}
        labels = list(data.keys())
        values = list(data.values())

        chart = BarChart(
            values=values,
            bar_names=labels,
            y_range=[0, 10, 2],
            y_length=5,
            x_length=9,
            x_axis_config={"font_size": 36},
            bar_colors=[BLUE, GREEN, RED, YELLOW, PURPLE],
        )

        title = Text("Weekly Activity", font_size=48).to_edge(UP)
        check_in_frame(title, "title")
        check_in_frame(chart, "chart")
        check_no_overlaps([title, chart], ["title", "chart"])
        self.play(Write(title))
        self.play(Create(chart), run_time=2)

        new_values = [v * 1.5 for v in values]
        self.wait()
        self.play(chart.animate.change_bar_values(new_values), run_time=2)

        bar_labels = chart.get_bar_labels(font_size=30)
        self.play(Write(bar_labels))
        self.wait(2)
```

---

## 5. Equation derivation step-by-step

```python
from manim import *

class QuadraticFormula(Scene):
    def construct(self):
        steps = [
            r"ax^2 + bx + c = 0",
            r"x^2 + \frac{b}{a}x + \frac{c}{a} = 0",
            r"x^2 + \frac{b}{a}x = -\frac{c}{a}",
            r"x^2 + \frac{b}{a}x + \frac{b^2}{4a^2} = \frac{b^2}{4a^2} - \frac{c}{a}",
            r"\left(x + \frac{b}{2a}\right)^2 = \frac{b^2 - 4ac}{4a^2}",
            r"x + \frac{b}{2a} = \pm\frac{\sqrt{b^2 - 4ac}}{2a}",
            r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
        ]

        annotations = [
            "Standard form", "Divide by a", "Move constant",
            "Complete the square", "Factor left side",
            "Take square root", "Quadratic formula",
        ]

        current = MathTex(steps[0]).scale(1.2)
        note = Text(annotations[0], font_size=30, color=GRAY).to_edge(DOWN)
        check_in_frame(current, "eq_0")
        check_in_frame(note, "note")
        check_no_overlaps([current, note], ["eq", "note"])
        self.play(Write(current), FadeIn(note))
        self.wait(1.5)

        for step, ann in zip(steps[1:], annotations[1:]):
            next_eq = MathTex(step).scale(1.2)
            next_note = Text(ann, font_size=30, color=GRAY).to_edge(DOWN)
            self.play(
                TransformMatchingTex(current, next_eq),
                FadeTransform(note, next_note),
                run_time=1.5
            )
            current = next_eq
            note = next_note
            self.wait(1)

        box = SurroundingRectangle(current, color=YELLOW, buff=0.2)
        self.play(Create(box))
        self.wait(2)
```

---

## 6. Network / graph visualization

```python
from manim import *

class GraphVisualization(Scene):
    def construct(self):
        vertices = [1, 2, 3, 4, 5]
        edges = [(1, 2), (1, 3), (2, 4), (3, 4), (4, 5), (2, 5)]

        g = Graph(
            vertices,
            edges,
            layout="spring",
            layout_scale=2.5,
            vertex_config={"radius": 0.3, "color": BLUE},
            edge_config={"color": WHITE, "stroke_width": 2},
            labels=True,
        )

        check_in_frame(g, "graph")
        self.play(Create(g), run_time=2)
        self.wait()

        path_edges = [(1, 2), (2, 4), (4, 5)]
        self.play(
            *[g.edges[e].animate.set_color(RED) for e in path_edges],
            *[g.vertices[v].animate.set_color(RED) for v in [1, 2, 4, 5]],
            run_time=1.5
        )
        self.wait(2)
```
