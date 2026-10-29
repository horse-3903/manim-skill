# ManimCE: Camera Deep Reference

**Import:** `from manim import *`

## Default Scene camera

The default `Scene` has a fixed camera. Move objects into view rather than moving the camera.

Frame dimensions: 14.22 × 8 units (16:9, independent of render resolution).

```python
# Access frame dimensions
frame_w = self.camera.frame_width   # 14.222...
frame_h = self.camera.frame_height  # 8.0
```

---

## MovingCameraScene

Lets you animate the camera frame itself. The camera is `self.camera.frame`.

```python
class PanAndZoom(MovingCameraScene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))

        # Zoom in
        self.play(self.camera.frame.animate.scale(0.5))

        # Pan right
        self.play(self.camera.frame.animate.shift(RIGHT * 3))

        # Zoom out and center
        self.play(self.camera.frame.animate.scale(2).move_to(ORIGIN))
```

`self.camera.frame` is a `Rectangle` mobject: any `.animate` call works on it.

Note: In ManimGL this is `self.frame` (no `.camera`).

---

## Follow a mobject

```python
class FollowDot(MovingCameraScene):
    def construct(self):
        dot = Dot(LEFT * 5)
        path = Line(LEFT * 5, RIGHT * 5)

        self.camera.frame.save_state()
        self.camera.frame.move_to(dot)

        self.camera.frame.add_updater(lambda f: f.move_to(dot))
        self.play(MoveAlongPath(dot, path), run_time=4, rate_func=linear)
        self.camera.frame.clear_updaters()

        self.play(Restore(self.camera.frame))
```

---

## ZoomedScene

Built-in split-screen zoom with a magnifying inset.

```python
class ZoomExample(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.3,
            zoomed_display_height=2,
            zoomed_display_width=3,
            image_frame_stroke_width=20,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
            },
            **kwargs
        )

    def construct(self):
        dot = Dot().shift(LEFT)
        self.add(dot)
        self.activate_zooming(animate=False)
        self.play(self.get_zoomed_display_pop_out_animation())
        self.zoomed_camera.frame.move_to(dot)
        self.wait(2)
```

---

## 3D camera: ThreeDScene

```python
class SurfacePlot(ThreeDScene):
    def construct(self):
        # phi: angle from vertical (0=top, 90=side)
        # theta: azimuth (horizontal rotation)
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        surface = Surface(
            lambda u, v: np.array([u, v, np.sin(u) * np.cos(v)]),
            u_range=[-PI, PI],
            v_range=[-PI, PI],
            resolution=(30, 30),
        )
        surface.set_style(fill_opacity=0.8)
        self.play(Create(surface), run_time=3)
```

**Camera movement in 3D:**
```python
# Rotate to new orientation
self.move_camera(phi=60 * DEGREES, theta=30 * DEGREES, run_time=2)

# Continuous slow rotation
self.begin_ambient_camera_rotation(rate=0.2)   # radians/sec
self.wait(4)
self.stop_ambient_camera_rotation()
```

---

## 3D objects

```python
Sphere(radius=1, color=BLUE)
Cylinder(radius=0.5, height=2)
Cone(base_radius=1, height=2)
Torus(major_radius=2, minor_radius=0.5)
Prism(dimensions=[2, 1, 1])
Arrow3D(start=ORIGIN, end=RIGHT * 2)
```

3D axes:
```python
axes = ThreeDAxes(
    x_range=[-3, 3],
    y_range=[-3, 3],
    z_range=[-2, 2],
)
self.add(axes)
```

---

## Background color

```python
class DarkScene(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        # or
        config.background_color = WHITE
```

Global in script:
```python
config.background_color = BLACK  # before scene class
```

---

## Sections and partial rendering

Mark named sections for partial re-render:
```python
def construct(self):
    self.next_section("Intro")
    # ... intro animations

    self.next_section("Main", skip_animations=True)
    # ... skip this section when testing
    self.next_section("Outro")
    # ... outro
```

---

## config flags reference

```bash
manim scene.py MyScene -p        # preview after render
manim scene.py MyScene -a        # render all scenes in file
manim scene.py MyScene --save_last_frame   # render PNG only
manim scene.py MyScene -n 10,20  # render only frames 10-20
manim scene.py MyScene --format gif
manim scene.py MyScene --transparent   # RGBA background
```

Quality flags: `-ql` (480p), `-qm` (720p), `-qh` (1080p), `-qk` (4K).

Resolution via config:
```python
config.pixel_height = 1080
config.pixel_width = 1920
config.frame_rate = 60
```
