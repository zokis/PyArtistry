import math

from PIL import Image, ImageDraw

DEGREES = "DEGREES"
RADIANS = "RADIANS"

RGB = "RGB"
HSB = "HSB"
HSL = "HSL"

CORNER = "CORNER"
CORNERS = "CORNERS"
CENTER = "CENTER"
RADIUS = "RADIUS"


def matrix_multiply(A, B):
    return [
        [sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*B)] for A_row in A
    ]


def hsb_to_rgb(h, s, v):
    h = h % 360
    s = s / 100
    v = v / 100

    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    return int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)


def hsl_to_rgb(h, s, l):
    h = h % 360
    s = s / 100
    l = l / 100

    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2

    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    return int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)


class Color:
    def __init__(self, r, g, b, a=255, color_mode=RGB, color_max=255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        self.color_mode = color_mode
        self.color_max = color_max

    def __str__(self):
        return f"Color({self.r}, {self.g}, {self.b}, {self.a})"

    def get_rgba(self):
        if self.color_mode == RGB:
            return (self.r, self.g, self.b, self.a)
        elif self.color_mode == HSB:
            return hsb_to_rgb(self.r, self.g, self.b) + (self.a,)
        elif self.color_mode == HSL:
            return hsl_to_rgb(self.r, self.g, self.b) + (self.a,)


class ColorNone(Color):
    def __init__(self):
        pass

    def get_rgba(self):
        return None

class PGlobals:
    background_color = Color(245, 225, 135)
    stroke_color = Color(100, 215, 225)
    fill_color = Color(150, 35, 195)
    width = 400
    height = 400
    stroke_width = 1
    draw = None
    canvas = None
    _transform_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    transform_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    angle_mode = RADIANS
    rotation_angle = 0
    color_mode = RGB
    color_max = 255
    shape_vertices = []
    state_stack = []
    rect_mode = CORNER
    ellipse_mode = CENTER
    scale_x = 1
    scale_y = 1

    @staticmethod
    def from_state(state):
        new_pg = PGlobals()
        new_pg.background_color = state["background_color"]
        new_pg.stroke_color = state["stroke_color"]
        new_pg.fill_color = state["fill_color"]
        new_pg.width = state["width"]
        new_pg.height = state["height"]
        new_pg.stroke_width = state["stroke_width"]
        new_pg.draw = state["draw"]
        new_pg.canvas = state["canvas"]
        new_pg.transform_matrix = state["transform_matrix"]
        new_pg.rect_mode = state["rect_mode"]
        new_pg.ellipse_mode = state["ellipse_mode"]
        new_pg.angle_mode = state["angle_mode"]
        new_pg.rotation_angle = state["rotation_angle"]
        new_pg.color_mode = state["color_mode"]
        new_pg.color_max = state["color_max"]
        new_pg.scale_x = state["scale_x"]
        new_pg.scale_y = state["scale_y"]
        return new_pg

    def get_state(self):
        return {
            "background_color": self.background_color,
            "stroke_color": self.stroke_color,
            "fill_color": self.fill_color,
            "width": self.width,
            "height": self.height,
            "stroke_width": self.stroke_width,
            "draw": self.draw,
            "canvas": self.canvas,
            "transform_matrix": self.transform_matrix,
            "rect_mode": self.rect_mode,
            "ellipse_mode": self.ellipse_mode,
            "angle_mode": self.angle_mode,
            "rotation_angle": self.rotation_angle,
            "color_mode": self.color_mode,
            "color_max": self.color_max,
            "scale_x": self.scale_x,
            "scale_y": self.scale_y,
        }

    def pop(self):
        if self.state_stack:
            state = self.state_stack.pop()
            self.background_color = state["background_color"]
            self.stroke_color = state["stroke_color"]
            self.fill_color = state["fill_color"]
            self.width = state["width"]
            self.height = state["height"]
            self.stroke_width = state["stroke_width"]
            self.draw = state["draw"]
            self.canvas = state["canvas"]
            self.transform_matrix = state["transform_matrix"]
            self.rect_mode = state["rect_mode"]
            self.ellipse_mode = state["ellipse_mode"]
            self.angle_mode = state["angle_mode"]
            self.rotation_angle = state["rotation_angle"]
            self.color_mode = state["color_mode"]
            self.color_max = state["color_max"]
            self.scale_x = state["scale_x"]
            self.scale_y = state["scale_y"]
        else:
            raise ValueError("No state to pop. Make sure to call push() before pop().")

    def push(self):
        self.state_stack.append(self.get_state())

    def show(self):
        self.canvas.show()

    def save(self, path):
        self.canvas.save(path)

    def get_center(self, points):
        min_x = min(points, key=lambda p: p[0])[0]
        max_x = max(points, key=lambda p: p[0])[0]
        min_y = min(points, key=lambda p: p[1])[1]
        max_y = max(points, key=lambda p: p[1])[1]
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        return center_x, center_y

    def apply_transform(self, points):
        if self.scale_x != 1 or self.scale_y != 1:
            center_x, center_y = self.get_center(points)
            scaled_points = [
                (
                    (x - center_x) * pg.scale_x + center_x,
                    (y - center_y) * pg.scale_y + center_y,
                )
                for x, y in points
            ]
        else:
            scaled_points = points

        if self._transform_matrix != self.transform_matrix:
            transformed_points = []
            for x, y in scaled_points:
                transformed_point = [
                    sum(a * b for a, b in zip(row, [x, y, 1]))
                    for row in self.transform_matrix
                ]
                transformed_points.append((transformed_point[0], transformed_point[1]))
            return transformed_points
        return [(int(p0), int(p1)) for p0, p1 in points]

    def convert_color(self, r, g, b):
        if g is None and b is None:
            g = b = r
        if self.color_mode == RGB:
            return (
                r * 255 // self.color_max,
                g * 255 // self.color_max,
                b * 255 // self.color_max,
            )
        elif self.color_mode == HSB:
            return hsb_to_rgb(r, g, b)
        elif self.color_mode == HSL:
            return hsl_to_rgb(r, g, b)


pg = PGlobals()


def show():
    pg.show()


def save(path: str):
    pg.save(path)


def push():
    pg.push()


def pop():
    pg.pop()


def rectMode(mode: str):
    if mode in [CORNER, CORNERS, CENTER, RADIUS]:
        pg.rect_mode = mode
    else:
        raise ValueError(
            "Invalid rectMode. Use 'CORNER', 'CORNERS', 'CENTER', or 'RADIUS'."
        )


def ellipseMode(mode: str):
    if mode in [CORNER, CORNERS, CENTER, RADIUS]:
        pg.ellipse_mode = mode
    else:
        raise ValueError(
            "Invalid ellipseMode. Use 'CORNER', 'CORNERS', 'CENTER', or 'RADIUS'."
        )


def colorMode(mode: str, max_val=None):
    if mode in [RGB, HSB, HSL]:
        pg.color_mode = mode
        if mode == RGB and max_val is not None:
            pg.color_max = max_val
    else:
        raise ValueError("Invalid color mode. Use 'RGB', 'HSB', or 'HSL'.")


def lerp(start: float, stop: float, amt: float) -> float:
    return amt * (stop - start) + start


def invLerp(start: float, stop: float, amt: float) -> float:
    return amt * (start - stop) + stop


def lerpColor(c1: Color, c2: Color, amt: float) -> Color:
    amt = max(0, min(amt, 1))
    rgba1 = c1.get_rgba()
    rgba2 = c2.get_rgba()
    return Color(
        int(lerp(rgba1[0], rgba2[0], amt)),
        int(lerp(rgba1[1], rgba2[1], amt)),
        int(lerp(rgba1[2], rgba2[2], amt)),
        int(lerp(rgba1[3], rgba2[3], amt)),
    )


def angleMode(mode=None):
    if mode is None:
        return pg.angle_mode
    if mode in [DEGREES, RADIANS]:
        pg.angle_mode = mode
    else:
        raise ValueError("Invalid angle mode. Use 'DEGREES' or 'RADIANS'.")


def scale(sx: int, sy=None):
    if sy is None:
        sy = sx
    pg.scale_x *= sx
    pg.scale_y *= sy


def translate(x: int, y: int):
    translation_matrix = [[1, 0, x], [0, 1, y], [0, 0, 1]]
    pg.transform_matrix = matrix_multiply(pg.transform_matrix, translation_matrix)


def rotate(angle: float):
    if pg.angle_mode == DEGREES:
        angle = math.radians(angle)
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    rotation_matrix = [[cos_angle, -sin_angle, 0], [sin_angle, cos_angle, 0], [0, 0, 1]]
    pg.transform_matrix = matrix_multiply(pg.transform_matrix, rotation_matrix)


def createCanvas(w: int, h: int):
    pg.width, pg.height = w, h
    pg.canvas = Image.new("RGBA", (pg.width, pg.height), pg.background_color.get_rgba())
    pg.draw = ImageDraw.Draw(pg.canvas)


def color(r, g, b, a=255):
    return Color(r, g, b, a, color_mode=pg.color_mode, color_max=pg.color_max)


def fill(r, g=None, b=None):
    if isinstance(r, Color):
        pg.fill_color = r
    else:
        pg.fill_color = Color(*pg.convert_color(r, g, b))


def noFill():
    pg.fill_color = ColorNone()


def stroke(r, g=None, b=None):
    if isinstance(r, Color):
        pg.stroke_color = r
    else:
        pg.stroke_color = Color(*pg.convert_color(r, g, b))


def strokeWeight(w: int):
    pg.stroke_width = w


def noStroke():
    pg.stroke_width = 0


def square(x: int, y: int, s: int):
    rect(x, y, s, s)


def rect(x: int, y: int, w: int, h: int):
    if pg.rect_mode == CENTER:
        x -= w / 2
        y -= h / 2
    elif pg.rect_mode == RADIUS:
        x -= w
        y -= h
        w *= 2
        h *= 2
    elif pg.rect_mode == CORNERS:
        w = w - x
        h = h - y

    pg.draw.polygon(
        pg.apply_transform([(x, y), (x + w, y), (x + w, y + h), (x, y + h)]),
        fill=pg.fill_color.get_rgba(),
        outline=pg.stroke_color.get_rgba(),
        width=pg.stroke_width,
    )


def triangle(x1, y1: int, x2: int, y2: int, x3: int, y3: int):
    pg.draw.polygon(
        pg.apply_transform([(x1, y1), (x2, y2), (x3, y3)]),
        fill=pg.fill_color.get_rgba(),
        outline=pg.stroke_color.get_rgba(),
        width=pg.stroke_width,
    )


def quad(x1, y1: int, x2: int, y2: int, x3: int, y3: int, x4: int, y4: int):
    pg.draw.polygon(
        pg.apply_transform([(x1, y1), (x2, y2), (x3, y3), (x4, y4)]),
        fill=pg.fill_color.get_rgba(),
        outline=pg.stroke_color.get_rgba(),
        width=pg.stroke_width,
    )

def line(x1: int, y1: int, x2: int, y2: int):
    pg.draw.line((x1, y1, x2, y2), fill=pg.stroke_color.get_rgba(), width=pg.stroke_width)


def circle(x: int, y: int, r: int):
    ellipse(x, y, r, r)


def ellipse(x: int, y: int, w: int, h: int):
    if pg.ellipse_mode == CENTER:
        bbox = [x - w // 2, y - h // 2, x + w // 2, y + h // 2]
    elif pg.ellipse_mode == RADIUS:
        bbox = [x - w, y - h, x + w, y + h]
    elif pg.ellipse_mode == CORNER:
        bbox = [x, y, x + w, y + h]
    elif pg.ellipse_mode == CORNERS:
        bbox = [x, y, w, h]
    pg.draw.ellipse(
        pg.apply_transform([bbox[:2], bbox[2:]]),
        fill=pg.fill_color.get_rgba(),
        outline=pg.stroke_color.get_rgba(),
        width=pg.stroke_width,
    )


def point(x: int, y: int):
    pg.draw.point((x, y), fill=pg.stroke_color.get_rgba())


def beginShape():
    pg.shape_vertices = []


def vertex(x: int, y: int):
    pg.shape_vertices.append((x, y))


def endShape(close: bool = False):
    if close:
        pg.draw.polygon(
            pg.shape_vertices,
            fill=pg.fill_color.get_rgba(),
            outline=pg.stroke_color.get_rgba(),
            width=pg.stroke_width,
        )
    else:
        for i in range(len(pg.shape_vertices) - 1):
            pg.draw.line(
                [
                    pg.shape_vertices[i],
                    pg.shape_vertices[i + 1],
                ],
                fill=pg.stroke_color,
                width=pg.stroke_width,
            )

    pg.shape_vertices = []


def background(r, g=None, b=None):
    if isinstance(r, Color):
        pg.draw.rectangle([0, 0, pg.width, pg.height], fill=r.get_rgba())
    else:
        pg.draw.rectangle([0, 0, pg.width, pg.height], fill=pg.convert_color(r, g, b))


def sin(angle: float) -> float:
    if pg.angle_mode == DEGREES:
        angle = math.radians(angle)
    return math.sin(angle)


def cos(angle: float) -> float:
    if pg.angle_mode == DEGREES:
        angle = math.radians(angle)
    return math.cos(angle)


def tan(angle: float) -> float:
    if pg.angle_mode == DEGREES:
        angle = math.radians(angle)
    return math.tan(angle)


def remap(
    value: float,
    start1: float,
    stop1: float,
    start2: float,
    stop2: float,
    within_bounds=False,
) -> float:
    mapped_value = start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))
    if within_bounds:
        if start2 < stop2:
            return max(min(mapped_value, stop2), start2)
        return max(min(mapped_value, start2), stop2)
    return mapped_value


def dist(x1: int, y1: int, x2: int, y2: int) -> int:
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def saveGif(
    draw_func,
    filename: str,
    size: tuple = (400, 400),
    max_frames: int = 100,
    frame_rate: int = 60,
):
    global pg
    pg = PGlobals.from_state(pg.get_state())

    frames = []

    for frameCount in range(max_frames):
        createCanvas(*size)
        draw_func(frameCount)
        frames.append(pg.canvas)

    frames[0].save(
        filename,
        save_all=True,
        append_images=frames[1:],
        duration=1000 / frame_rate,
        loop=0,  # loop forever
    )
