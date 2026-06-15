"""
Linear Regression -- Step-by-Step Manim Animation
Scene: LinearRegressionStepByStep

Render:
    manim -pqh demos/linear_regression/linear_regression.py LinearRegressionStepByStep
"""

from manim import *
import numpy as np

np.random.seed(42)


def _make_data(n=12, x_lo=0.3, x_hi=4.7, true_w=0.65, true_b=0.9, noise_std=0.62):
    """Generate scattered points with a linear trend. Adjust noise_std for r ~ 0.85-0.90."""
    x = np.sort(np.random.uniform(x_lo, x_hi, n))
    y = true_w * x + true_b + np.random.normal(0, noise_std, n)
    w_fit, b_fit = np.polyfit(x, y, 1)
    return x, y, round(w_fit, 2), round(b_fit, 2)


_X, _Y, _W_FIT, _B_FIT = _make_data()

FRAME_X_LIMIT = 7.0
FRAME_Y_LIMIT = 3.8


def check_in_frame(mob, name="mob"):
    l = mob.get_left()[0]
    r = mob.get_right()[0]
    b = mob.get_bottom()[1]
    t = mob.get_top()[1]
    issues = []
    if l < -FRAME_X_LIMIT:
        issues.append(f"left {l:.2f}")
    if r > FRAME_X_LIMIT:
        issues.append(f"right {r:.2f}")
    if b < -FRAME_Y_LIMIT:
        issues.append(f"bottom {b:.2f}")
    if t > FRAME_Y_LIMIT:
        issues.append(f"top {t:.2f}")
    if issues:
        print(f"[LAYOUT WARNING] '{name}' out of frame: {issues}")
    return not issues


class LinearRegressionStepByStep(Scene):
    """
    Walks through linear regression from data -> line -> residuals -> squared loss ->
    optimisation, using fully synthetic data and no external dependencies.
    """

    X, Y = _X, _Y
    W_FIT, B_FIT = _W_FIT, _B_FIT

    W_INIT = 0.38
    B_INIT = 1.60

    # ── helpers ──────────────────────────────────────────────────────────────

    def _axes(self):
        # Large axes filling the left portion of the frame
        ax = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=6.5,
            y_length=5.2,
            axis_config={"color": WHITE, "stroke_width": 2, "include_tip": True},
        ).move_to(LEFT * 1.5 + DOWN * 0.2)
        return ax

    def _dots(self, ax):
        return VGroup(*[
            Dot(ax.c2p(x, y), color=BLUE, radius=0.09)
            for x, y in zip(self.X, self.Y)
        ])

    def _line(self, ax, w, b, color=YELLOW, opacity=1.0):
        g = ax.plot(lambda x: w * x + b, x_range=[0.05, 4.75], color=color, stroke_width=3)
        g.set_stroke(opacity=opacity)
        return g

    def _residuals(self, ax, w, b, color=RED):
        segs = VGroup()
        for x, y in zip(self.X, self.Y):
            yp = w * x + b
            segs.add(Line(ax.c2p(x, y), ax.c2p(x, yp), color=color, stroke_width=2.5))
        return segs

    def _error_squares(self, ax, w, b):
        squares = VGroup()
        for x, y in zip(self.X, self.Y):
            yp = w * x + b
            p_actual = np.array(ax.c2p(x, y))
            p_pred = np.array(ax.c2p(x, yp))
            h = abs(p_actual[1] - p_pred[1])
            if h < 0.02:
                continue
            mid = (p_actual + p_pred) / 2
            sq = Square(side_length=h).move_to(mid)
            sq.shift(LEFT * h / 2)
            sq.set_fill(RED, opacity=0.28).set_stroke(RED, width=1.5)
            squares.add(sq)
        return squares

    # ── main construct ────────────────────────────────────────────────────────

    def construct(self):
        self.camera.background_color = BLACK

        ax = self._axes()
        x_lbl = ax.get_x_axis_label(Text("x", font_size=22, color=GREY_A))
        y_lbl = ax.get_y_axis_label(
            Text("y", font_size=22, color=GREY_A), edge=LEFT, direction=LEFT
        )
        dots = self._dots(ax)

        check_in_frame(ax, "axes")

        # ── Step 1: Introduce the problem ─────────────────────────────────────
        title = Text("Linear Regression", font_size=36, color=WHITE).to_edge(UP, buff=0.3)
        subtitle = Text("Predicting a continuous value", font_size=26, color=GREY_A)
        subtitle.next_to(title, DOWN, buff=0.15)

        check_in_frame(title, "title")

        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(subtitle, shift=UP * 0.15))
        self.play(Create(ax), Write(x_lbl), Write(y_lbl), run_time=1.5)
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.08), run_time=1.2)
        self.wait()

        question = Text(
            "Can we find a line\nthat predicts y from x?",
            font_size=24, color=YELLOW,
        ).move_to(RIGHT * 4.3 + DOWN * 0.5)
        check_in_frame(question, "question")
        self.play(Write(question), run_time=1.2)
        self.wait(2)
        self.play(FadeOut(question), FadeOut(subtitle))

        # ── Step 2: Candidate line ────────────────────────────────────────────
        s2_lbl = Text("A Candidate Line", font_size=36, color=YELLOW).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title, s2_lbl))

        init_line = self._line(ax, self.W_INIT, self.B_INIT)
        formula = MathTex(r"\hat{y} = wx + b", font_size=36, color=YELLOW)
        formula.move_to(RIGHT * 4.3 + UP * 1.6)
        check_in_frame(formula, "formula")

        self.play(Create(init_line), run_time=1.5)
        self.play(Write(formula))
        self.wait()

        # Slope triangle
        x1, x2 = 1.5, 2.5
        y1p = self.W_INIT * x1 + self.B_INIT
        y2p = self.W_INIT * x2 + self.B_INIT
        tri = Polygon(
            ax.c2p(x1, y1p), ax.c2p(x2, y1p), ax.c2p(x2, y2p),
            color=YELLOW, stroke_width=2,
        ).set_fill(YELLOW, opacity=0.12)
        w_ann = Text("slope  w", font_size=20, color=YELLOW)
        w_ann.next_to(ax.c2p(x2, (y1p + y2p) / 2), RIGHT, buff=0.12)

        b_dot = Dot(ax.c2p(0, self.B_INIT), color=ORANGE, radius=0.12)
        b_ann = Text("intercept  b", font_size=20, color=ORANGE)
        b_ann.next_to(b_dot, RIGHT, buff=0.1)

        check_in_frame(w_ann, "w_ann")

        self.play(Create(tri), Write(w_ann))
        self.play(FadeIn(b_dot), Write(b_ann))
        self.wait(2)
        self.play(FadeOut(VGroup(tri, w_ann, b_dot, b_ann)))

        # ── Step 3: Predictions for sample x-values ──────────────────────────
        s3_lbl = Text("Predictions for Every x", font_size=36, color=YELLOW).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(s2_lbl, s3_lbl))

        note3 = Text("The line gives a prediction\nfor every x.", font_size=22, color=GREY_A)
        note3.move_to(RIGHT * 4.3 + UP * 0.8)
        self.play(Write(note3))

        sample_xs = [1.0, 2.5, 4.0]
        colors3 = [TEAL_C, GREEN_C, PINK]
        proj = VGroup()

        for i, (sx, sc) in enumerate(zip(sample_xs, colors3)):
            syp = self.W_INIT * sx + self.B_INIT
            v = DashedLine(ax.c2p(sx, 0), ax.c2p(sx, syp), color=sc, stroke_width=1.8, dash_length=0.1)
            h = DashedLine(ax.c2p(0, syp), ax.c2p(sx, syp), color=sc, stroke_width=1.8, dash_length=0.1)
            pd = Dot(ax.c2p(sx, syp), color=sc, radius=0.1)
            lbl = MathTex(rf"\hat{{y}}_{i + 1}", font_size=22, color=sc)
            lbl.next_to(pd, UP, buff=0.12)  # above predicted dot, not left of y-axis (avoids y_lbl collision)
            proj.add(v, h, pd, lbl)
            self.play(Create(v), Create(h), FadeIn(pd), Write(lbl), run_time=0.7)

        self.wait(2)
        self.play(FadeOut(proj), FadeOut(note3))

        # ── Step 4: Residual errors ───────────────────────────────────────────
        s4_lbl = Text("Residual Errors", font_size=36, color=YELLOW).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(s3_lbl, s4_lbl))

        residuals = self._residuals(ax, self.W_INIT, self.B_INIT)
        err_fml = MathTex(r"\text{error} = y - \hat{y}", font_size=32, color=RED)
        err_fml.move_to(RIGHT * 4.3 + UP * 1.6)
        check_in_frame(err_fml, "err_fml")

        self.play(FadeOut(formula))
        for seg in residuals:
            self.play(Create(seg), run_time=0.14)
        self.play(Write(err_fml))
        self.wait(2)

        # ── Step 5: Squared error intuition ──────────────────────────────────
        s5_lbl = Text("Squared Error  (the Loss)", font_size=36, color=YELLOW).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(s4_lbl, s5_lbl))

        squares = self._error_squares(ax, self.W_INIT, self.B_INIT)
        loss_fml = MathTex(r"\mathcal{L} = \sum_i (y_i - \hat{y}_i)^2", font_size=30, color=WHITE)
        loss_fml.move_to(RIGHT * 4.2 + UP * 1.6)
        heavy = Text("Large errors are\npenalised much more!", font_size=22, color=RED)
        heavy.move_to(RIGHT * 4.2 + DOWN * 0.1)

        check_in_frame(loss_fml, "loss_fml")
        check_in_frame(heavy, "heavy")

        self.play(FadeOut(err_fml))
        self.play(FadeIn(squares), run_time=1.2)
        self.play(Write(loss_fml))
        self.play(Write(heavy))
        self.wait(2)
        self.play(FadeOut(VGroup(squares, heavy, loss_fml)))  # must clear loss_fml before step 6 reuses its position

        # ── Step 6: Optimisation ─────────────────────────────────────────────
        s6_lbl = Text("Minimise the Loss -- Find the Best Line", font_size=32, color=YELLOW)
        s6_lbl.to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(s5_lbl, s6_lbl))

        bad_lines = VGroup()
        for i, (w, b, lstr, col) in enumerate([
            (1.40, 0.10, "Loss ~ 52", GREY_C),
            (1.00, 0.45, "Loss ~ 21", GREY_B),
        ]):
            cl = self._line(ax, w, b, color=col, opacity=0.55)
            lt = Text(lstr, font_size=22, color=col)
            lt.move_to(RIGHT * 4.3 + UP * (1.6 - i * 0.6))
            bad_lines.add(cl, lt)
            self.play(Create(cl), Write(lt), run_time=0.7)

        self.wait()
        self.play(FadeOut(bad_lines), FadeOut(init_line), FadeOut(residuals))

        best_line = self._line(ax, self.W_FIT, self.B_FIT, color=YELLOW)
        best_res = self._residuals(ax, self.W_FIT, self.B_FIT)
        best_loss = Text("Loss ~ 8  (minimum)", font_size=24, color=GREEN)
        best_loss.move_to(RIGHT * 4.3 + UP * 1.6)
        opt_note = Text(
            "Choose  w,  b  that \nminimise total \nsquared error.",
            font_size=24, color=WHITE,
        ).move_to(RIGHT * 4.3 + DOWN * 0.3)

        check_in_frame(opt_note, "opt_note")

        self.play(Create(best_line), run_time=1.5)
        self.play(LaggedStartMap(FadeIn, best_res, lag_ratio=0.08))
        self.play(Write(best_loss), Write(opt_note))
        self.wait(2)

        # ── Step 7: Summary ───────────────────────────────────────────────────
        self.play(
            FadeOut(VGroup(
                s6_lbl, best_loss, opt_note,
                best_res, dots, ax, x_lbl, y_lbl, best_line,
            ))
        )

        sum_title = Text("Linear Regression  --  Summary", font_size=36, color=YELLOW).to_edge(UP, buff=0.35)
        self.play(Write(sum_title))

        # All MathTex so font sizes render consistently (Text and MathTex scale differently)
        steps = VGroup(
            MathTex(r"1 \quad \text{Data points with an upward trend}", font_size=36, color=BLUE),
            MathTex(r"2 \quad \hat{y} = wx + b \ \text{-- fit a straight line}", font_size=36, color=YELLOW),
            MathTex(r"3 \quad \text{error} = y - \hat{y} \ \text{-- residuals}", font_size=36, color=RED),
            MathTex(r"4 \quad \mathcal{L} = \sum (y_i - \hat{y}_i)^2 \ \text{-- loss}", font_size=36, color=WHITE),
            MathTex(r"5 \quad \text{Optimise: choose } w, b \text{ to minimise } \mathcal{L}", font_size=36, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).center().shift(UP * 0.5)

        steps.set_width(min(steps.get_width(), 12.5))
        check_in_frame(steps, "steps")
        self.play(LaggedStartMap(FadeIn, steps, shift=RIGHT * 0.3, lag_ratio=0.22), run_time=2.5)
        self.wait(3)
