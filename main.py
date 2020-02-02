from tkinter import *


class SierpinskiTriangle():

    def __init__(self):
        self.MIN_DEPTH = 3
        self.MAX_DEPTH = 8
        self.depth = self.MIN_DEPTH
        self.length = 400
        self.points = self._get_points(77, 400, self.length)
        self.moved_points = []
        self.scale_value = 1

    def _scale(self, scale_factor):
        increment = scale_factor * self.length
        if scale_factor > 1:
            scaled_length = self.length + increment
        else:
            scaled_length = self.length
        self.points = self._get_points(
            self.points[0][0],
            self.points[0][1],
            scaled_length
        )

    def _get_points(self, x, y, length):
        # x, y are the points of the lower left corner
        height = length * (3 ** .5) / 2  # (length * sqrt 3) / 2
        lower_left = [x, y]
        top = [x + length / 2, y - height]
        lower_right = [x + length, y]
        return [lower_left, lower_right, top]

    def _get_mid(self, a, b):
        return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)

    def _draw_triangle(self, points, canvas, colour="black"):
        canvas.create_polygon(
            points[0][0], points[0][1],  # x1 y1
            points[1][0], points[1][1],  # x2 y2
            points[2][0], points[2][1],  # x3 y3
            fill=colour
        )

    def _draw_fractal(self, canvas, points, depth):
        if depth == 0:
            self._draw_triangle(points, canvas)
        if depth > 0:
            self._draw_fractal(
                canvas,
                [points[0],
                self._get_mid(points[0], points[1]),
                self._get_mid(points[0], points[2])],
                depth - 1)

            self._draw_fractal(
                canvas,
                [points[1],
                self._get_mid(points[0], points[1]),
                self._get_mid(points[1], points[2])],
                depth - 1)

            self._draw_fractal(
                canvas,
                [points[2],
                self._get_mid(points[2], points[1]),
                self._get_mid(points[0], points[2])],
                depth - 1)

    def add_moved_points(self, x, y):
        self.moved_points.append([x, y])

    def draw(self, canvas):
        canvas.delete(ALL)
        self._scale(self.scale_value)
        self._draw_fractal(canvas, self.points, self.depth)

    def zoom_in(self):
        if self.depth < self.MAX_DEPTH:
            self.scale_value += 1
            self._scale(self.scale_value)
            self.depth += 1

    def zoom_out(self):
        if self.depth > self.MIN_DEPTH:
            self.scale_value -= 1
            self._scale(self.scale_value)
            self.depth -= 1

    def move(self):
        if len(self.moved_points) == 2:
            delta_x = self.moved_points[1][0] - self.moved_points[0][0]
            delta_y = self.moved_points[1][1] - self.moved_points[0][1]
            for point in self.points:
                point[0] += delta_x
                point[1] += delta_y
            self.moved_points = []


class Gui():

    def __init__(self, triangle):
        self.root = Tk()
        self.root.title("Sierpinski Triangle Explorer")
        self.canvas_width = 600
        self.canvas_height = 600
        self.triangle = triangle

        self.canvas = Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(fill="both", expand=True)

        button_frame = Frame(self.root)
        Button(button_frame, text='Zoom in', command=self.triangle.zoom_in).pack(side=LEFT)
        Button(button_frame, text='Zoom out', command=self.triangle.zoom_out).pack(side=LEFT)
        button_frame.pack(side=BOTTOM)

        self.root.bind("<Key>", lambda event: self.on_key_press(event))
        self.root.bind("<Button-1>", lambda event: self.on_button_press(event))
        self.root.bind("<ButtonRelease-1>", lambda event: self.on_button_release(event))

        self.triangle.draw(self.canvas)
        self.root.mainloop()

    def on_key_press(self, event):
        if event.keysym in ["Up"]:
            self.triangle.zoom_in()
        elif event.keysym in ["Down"]:
            self.triangle.zoom_out()
        self.triangle.draw(self.canvas)

    def on_button_press(self, event):
        self.triangle.add_moved_points(event.x, event.y)

    def on_button_release(self, event):
        self.triangle.add_moved_points(event.x, event.y)
        self.triangle.move()
        self.triangle.draw(self.canvas)


if __name__ == '__main__':
    triangle = SierpinskiTriangle()
    Gui(triangle)
