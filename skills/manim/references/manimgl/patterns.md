# ManimGL: Complete Working Examples

All examples use ManimGL (`from manimlib import *`).

---

## 1. Basic InteractiveScene

```python
from manimlib import *

class BasicExample(InteractiveScene):
    def construct(self):
        circle = Circle(color=BLUE)
        label = Tex(r"$\pi r^2$", font_size=72)

        self.play(ShowCreation(circle))
        self.play(Write(label))
        self.play(label.animate.next_to(circle, RIGHT))
        self.wait()
```

---

## 2. Camera frame control

```python
from manimlib import *

class CameraDemo(InteractiveScene):
    def construct(self):
        dots = VGroup(*[Dot(RIGHT * i) for i in range(-3, 4)])
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.1))
        self.wait()

        # Zoom in on center
        self.play(self.frame.animate.scale(0.5), run_time=2)
        self.wait()

        # Pan right
        self.play(self.frame.animate.shift(RIGHT * 3), run_time=2)
        self.wait()

        # Restore
        self.play(self.frame.animate.scale(2).move_to(ORIGIN), run_time=2)
        self.wait()
```

---

## 3. Equation derivation with Tex

```python
from manimlib import *

class QuadraticDerivation(InteractiveScene):
    def construct(self):
        COLOR_MAP = {"a": BLUE, "b": TEAL, "c": RED}

        steps = [
            Tex(r"$ax^2 + bx + c = 0$", t2c=COLOR_MAP),
            Tex(r"$x^2 + \frac{b}{a}x = -\frac{c}{a}$", t2c=COLOR_MAP),
            Tex(r"$\left(x + \frac{b}{2a}\right)^2 = \frac{b^2 - 4ac}{4a^2}$", t2c=COLOR_MAP),
            Tex(r"$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$", t2c=COLOR_MAP),
        ]

        current = steps[0].scale(1.2)
        self.play(Write(current))
        self.wait()

        for next_eq in steps[1:]:
            next_eq.scale(1.2)
            self.play(TransformMatchingStrings(current, next_eq))
            self.wait()
            current = next_eq

        box = SurroundingRectangle(current, color=YELLOW, buff=0.2)
        box.round_corners(radius=0.1)
        self.play(ShowCreation(box))
        self.wait(2)
```

---

## 4. ValueTracker + GlowDot on a graph

```python
from manimlib import *

class TrackerOnGraph(InteractiveScene):
    def construct(self):
        axes = Axes(x_range=(-4, 4), y_range=(-2, 2))
        graph = axes.get_graph(lambda x: np.sin(x), color=BLUE)
        self.add(axes)
        self.play(ShowCreation(graph), run_time=2)

        t = ValueTracker(0)

        dot = GlowDot(color=RED)
        dot.add_updater(lambda d: d.move_to(
            axes.input_to_graph_point(t.get_value(), graph)
        ))

        label = always_redraw(lambda: Tex(
            rf"$x = {t.get_value():.2f}$", font_size=36, color=RED
        ).next_to(dot, UP))

        self.add(dot, label)
        self.play(t.animate.set_value(4), run_time=5, rate_func=smooth)
        self.wait()
```

---

## 5. time_span for precise timing

```python
from manimlib import *

class TimeSpanExample(InteractiveScene):
    def construct(self):
        arrow = Arrow(LEFT * 2, RIGHT * 2, color=YELLOW)
        label = Tex(r"Look here!", font_size=48)
        box = SurroundingRectangle(label, color=YELLOW)

        self.play(
            ShowCreation(arrow, time_span=(0.0, 1.0)),
            Write(label, time_span=(0.5, 2.5)),
            ShowCreation(box, time_span=(2.0, 3.0)),
            run_time=3,
        )
        self.wait()
```

---

## 6. VShowPassingFlash: signal flow

```python
from manimlib import *

class SignalFlow(InteractiveScene):
    def construct(self):
        nodes = VGroup(*[Circle(radius=0.4, color=BLUE) for _ in range(4)])
        nodes.arrange(RIGHT, buff=1.5)
        self.play(LaggedStartMap(FadeIn, nodes, lag_ratio=0.2))

        # Signal traveling between nodes
        for i in range(len(nodes) - 1):
            line = Line(nodes[i].get_right(), nodes[i + 1].get_left())
            self.add(line)
            self.play(VShowPassingFlash(
                line.copy().set_stroke(YELLOW, 5),
                time_width=0.4,
                run_time=0.8,
            ))
        self.wait()
```

---

## 7. 3D scene

```python
from manimlib import *

class SurfaceDemo(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(x_range=(-2, 2), y_range=(-2, 2), z_range=(-2, 2))
        self.set_camera_orientation(phi=70 * DEGREES, theta=-60 * DEGREES)

        surface = ParametricSurface(
            lambda u, v: axes.c2p(u, v, u**2 - v**2),
            u_range=(-1.5, 1.5),
            v_range=(-1.5, 1.5),
            resolution=(20, 20),
        )
        surface.set_style(fill_opacity=0.85)

        self.play(ShowCreation(axes), ShowCreation(surface), run_time=3)
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(5)
        self.stop_ambient_camera_rotation()
```

---

## 8. Pythagorean theorem proof

```python
from manimlib import *

class PythagoreanProof(InteractiveScene):
    def construct(self):
        a, b = 3, 4
        triangle = Polygon(ORIGIN, RIGHT * a, RIGHT * a + UP * b, color=WHITE)
        self.play(ShowCreation(triangle))

        label_a = Tex(r"$a$", color=BLUE).next_to(triangle, DOWN)
        label_b = Tex(r"$b$", color=TEAL).next_to(triangle, RIGHT)
        label_c = Tex(r"$c$", color=RED).next_to(triangle.get_center(), UL)
        self.play(Write(label_a), Write(label_b), Write(label_c))
        self.wait()

        eq = Tex(r"$a^2 + b^2 = c^2$", t2c={"a": BLUE, "b": TEAL, "c": RED})
        eq.to_edge(UP)
        self.play(Write(eq))

        eq2 = Tex(rf"${a}^2 + {b}^2 = c^2$", t2c={"c": RED})
        eq2.to_edge(UP)
        eq3 = Tex(rf"${a**2} + {b**2} = c^2$", t2c={"c": RED})
        eq3.to_edge(UP)
        eq4 = Tex(rf"$c = {(a**2 + b**2)**0.5:.0f}$", t2c={"c": RED})
        eq4.to_edge(UP)

        for next_eq in [eq2, eq3, eq4]:
            self.play(TransformMatchingStrings(eq, next_eq))
            eq = next_eq
            self.wait(0.5)

        self.wait(2)
```
