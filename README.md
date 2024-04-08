# PyArtistry: A Python Library for Creative Coding

PyArtistry is a Python library inspired by the popular Processing and p5.js framework. Originally designed for a personal project to generate static images without user interaction. PyArtistry is free to use, and its continuation and evolution are welcome by the community.

To use PyArtistry, you need to have Python and the Pillow library installed. You can install Pillow using pip:
`pip install Pillow` 

## Getting Started

To start using PyArtistry, you first need to create a canvas where you can draw your shapes and images:

```
from pyartistry import *

createCanvas(400, 400)
```
## Drawing Shapes

PyArtistry provides various functions to draw shapes on the canvas:

### Rectangles

`rect(x, y, width, height)` 

-   `x`: The x-coordinate of the rectangle.
-   `y`: The y-coordinate of the rectangle.
-   `width`: The width of the rectangle.
-   `height`: The height of the rectangle.

### Circles

`circle(x, y, radius)` 

-   `x`: The x-coordinate of the circle's center.
-   `y`: The y-coordinate of the circle's center.
-   `radius`: The radius of the circle.

### Ellipses

`ellipse(x, y, width, height)` 

-   `x`: The x-coordinate of the ellipse's center.
-   `y`: The y-coordinate of the ellipse's center.
-   `width`: The width of the ellipse.
-   `height`: The height of the ellipse.

### Triangles

`triangle(x1, y1, x2, y2, x3, y3)` 

-   `x1`, `y1`: The coordinates of the first vertex.
-   `x2`, `y2`: The coordinates of the second vertex.
-   `x3`, `y3`: The coordinates of the third vertex.

### Quads

`quad(x1, y1, x2, y2, x3, y3, x4, y4)` 

-   `x1`, `y1`: The coordinates of the first vertex.
-   `x2`, `y2`: The coordinates of the second vertex.
-   `x3`, `y3`: The coordinates of the third vertex.
-   `x4`, `y4`: The coordinates of the fourth vertex.

### Lines

`line(x1, y1, x2, y2)` 

-   `x1`, `y1`: The coordinates of the start point.
-   `x2`, `y2`: The coordinates of the end point.

### Points

`point(x, y)` 

-   `x`: The x-coordinate of the point.
-   `y`: The y-coordinate of the point.

## Custom Shapes

-   `beginShape()`: Begins recording vertices for a shape.
-   `vertex(x, y)`: Specifies a vertex for the shape.
-   `endShape(close=False)`: Ends recording vertices and draws the shape. If `close` is `True`, the shape will be closed.

## Color

PyArtistry allows you to set colors for the shapes you draw:

### Fill Color

`fill(r, g, b)` 

-   `r`: The red component of the color (0-255).
-   `g`: The green component of the color (0-255).
-   `b`: The blue component of the color (0-255).

`noFill()` 

### Stroke Color

`stroke(r, g, b)` 

-   `r`: The red component of the stroke color (0-255).
-   `g`: The green component of the stroke color (0-255).
-   `b`: The blue component of the stroke color (0-255).

`noStroke()` 

### Stroke Weight

`strokeWeight(weight)` 

-   `weight`: The thickness of the stroke.

## Math

-   `sin(angle)`: Returns the sine of an angle.
-   `cos(angle)`: Returns the cosine of an angle.
-   `tan(angle)`: Returns the tangent of an angle.
-   `remap(value, start1, stop1, start2, stop2, withinBounds=False)`: Re-maps a number from one range to another.
-   `dist(x1, y1, x2, y2)`: Calculates the distance between two points in 2D.
-   `lerp(start, stop, amt)`: Linearly interpolates between two values.
-   `invLerp(start, stop, amt)`: Inverse linear interpolation between two values.
-   `lerpColor(c1, c2, amt)`: Linearly interpolates between two colors.

## Transformations

PyArtistry supports transformations such as translation, rotation, and scaling:

### Translate

`translate(x, y)` 

-   `x`: The amount to translate along the x-axis.
-   `y`: The amount to translate along the y-axis.

### Rotate

`rotate(angle)` 

-   `angle`: The angle of rotation in radians (use `radians(angle)` to convert degrees to radians).

### Scale

`scale(sx, sy)` 

-   `sx`: The scaling factor along the x-axis.
-   `sy`: The scaling factor along the y-axis.

## Displaying the Canvas

After drawing your shapes, you can display the canvas using the `show()` function:

`show()` 

## Saving the Canvas

You can save the canvas to an image file using the `save()` function:


`save("filename.png")` 

## Background

`background(r, g, b)` 

-   `r`: The red component of the background color (0-255).
-   `g`: The green component of the background color (0-255).
-   `b`: The blue component of the background color (0-255).

## Angle Mode

`angleMode(mode)` 

-   `mode`: Either `DEGREES` or `RADIANS`. Sets the mode for interpreting angles in trigonometric functions.

## Rectangle and Ellipse Modes

`rectMode(mode)` 

-   `mode`: One of `CORNER`, `CORNERS`, `CENTER`, or `RADIUS`. Sets the mode for drawing rectangles.


`ellipseMode(mode)` 

-   `mode`: One of `CORNER`, `CORNERS`, `CENTER`, or `RADIUS`. Sets the mode for drawing ellipses.

## Color Mode

`colorMode(mode, max_val=None)` 

-   `mode`: Either `RGB`, `HSB`, or `HSL`. Sets the mode for interpreting color values.
-   `max_val`: Optional. The maximum value for color components in `RGB` mode.

## State

-   `push()`: Saves the current drawing style settings and transformations.
-   `pop()`: Restores the saved drawing style settings and transformations.

## Example

Here's a simple example that draws a rectangle and a circle with different colors:

```python
from pyartistry import *

createCanvas(400, 400)
fill(255, 0, 0)
rect(100, 100, 200, 150)
fill(0, 0, 255)
circle(200, 200, 50)
show()
```

This will create a canvas with a red rectangle and a blue circle.

## Constants

-   `DEGREES`: Constant for setting angle mode to degrees.
-   `RADIANS`: Constant for setting angle mode to radians.
-   `RGB`: Constant for setting color mode to RGB.
-   `HSB`: Constant for setting color mode to HSB (Hue, Saturation, Brightness).
-   `HSL`: Constant for setting color mode to HSL (Hue, Saturation, Lightness).

## Noise Module

The Noise module in PyArtistry is used to generate Perlin noise, which is useful for creating natural-looking textures and patterns. Perlin noise is a type of gradient noise developed by Ken Perlin.

### Functions

#### `noise(x, y=0, z=0)`

Generates a Perlin noise value based on the input coordinates.

-   `x`: The x-coordinate of the noise sample.
-   `y`: The y-coordinate of the noise sample. Default is 0.
-   `z`: The z-coordinate of the noise sample. Default is 0.

Returns a noise value between 0 and 1.

#### `noiseSeed(seed)`

Sets the seed value for the Perlin noise function.

-   `seed`: The seed value for the noise generator.

This function allows you to get consistent noise values across different runs of your program.

### Example

```python
from pyartistry import noise, noiseSeed

noiseSeed(99)
n = noise(0.1, 0.2, 0.3)
print(n)  # Example output: 0.3778873367033471
```

### Notes

-   The `noise` function generates values between 0 and 1, which can be scaled and translated to fit any desired range.
-   The `noiseSeed` function is useful for creating reproducible noise patterns, which can be important in some applications.
-   Perlin noise can be used for various purposes, such as generating terrain, creating textures, or simulating natural phenomena like clouds and water.

## Saving GIFs

### `saveGif(draw_func, filename, size=(400, 400), max_frames=100, frame_rate=60)`

Generates a GIF by repeatedly calling a drawing function and saving the resulting frames.

-   `draw_func`: A function that takes a single argument `frameCount` and draws the content for each frame.
-   `filename`: The name of the output GIF file.
-   `size`: A tuple `(width, height)` specifying the size of each frame. Default is `(400, 400)`.
-   `max_frames`: The total number of frames in the GIF. Default is `100`.
-   `frame_rate`: The frame rate of the GIF in frames per second. Default is `60`.

This function creates a new canvas for each frame, calls the `draw_func` to draw the frame, and then appends the frame to the GIF. The GIF is saved with the specified `filename`.

### Example Usage

```python
from pyartistry import *

def draw(frameCount):
    background(200, 200, 200)

    c1 = color(155, 0, 255, 255)
    c2 = color(100, 255, 50, 255)

    fill(lerpColor(c1, c2, (1 / 8) * frameCount))
    translate(20, 20)
    quad(x1=40, y1=40, x2=50, y2=60, x3=30, y3=60, x4=30, y4=50)

saveGif(draw, "filename.gif", (255, 255), max_frames=8, frame_rate=1)
```

In this example, the `draw` function creates a series of frames with a quadrilateral that changes color over time. The `saveGif` function then generates a GIF with 8 frames at a frame rate of 1 frame per second.
