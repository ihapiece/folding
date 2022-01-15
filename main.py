import pyglet
import pyglet.graphics
from pyglet.window import mouse
from folding import *

def draw_line(a, b):
    if isinf(a.x+a.y+b.x+b.y):
        return
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
    ('v2i', (int(a.x), int(a.y), int(b.x), int(b.y))))

def draw_polygon(p):
    if len(p.vertices) == 0:
        return
    vp = p.vertices[-1]
    for v in p.vertices:
        draw_line(vp, v)
        vp = v

def draw_page(p):
    draw_polygon(p.part1)
    draw_polygon(p.part2)

window = pyglet.window.Window()

vertices = [Point(210, 110), Point(400, 110), Point(400, 220), Point(210, 220)]

page = Page(*vertices)
foldfrom = None

@window.event
def on_mouse_release(x, y, button, modifiers):
    global foldfrom
    foldfrom = None

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global foldfrom
    if foldfrom == None:
        foldfrom = Point(x, y)
    else:
        fold = Fold(foldfrom, Point(x, y))
        page.add_fold(fold)

@window.event
def on_draw():
    window.clear()
    draw_page(page)

pyglet.app.run()
