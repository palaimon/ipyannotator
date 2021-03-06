# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01_bbox_canvas.ipynb (unless otherwise specified).

__all__ = ['BBoxCanvas']

# Internal Cell
import numpy as np
import traitlets
import ipywidgets as widgets
from pathlib import Path
from math import log
from ipycanvas import MultiCanvas, hold_canvas
from ipywidgets import Image, Label, Layout, HBox, VBox, Output

# Internal Cell

def draw_bg(canvas, color='rgb(236,240,241)'):
    with hold_canvas(canvas):
        canvas.fill_style = color
        canvas.fill_rect(0, 0, canvas.size[0], canvas.size[1])

# Internal Cell

def draw_bounding_box(canvas, coords, color='white', line_width=None,
                      border_ratio=2, clear=False):
    with hold_canvas(canvas):
        if clear:
            canvas.clear()

        pos_x, pos_y, rect_x, rect_y = coords

        canvas.line_width = line_width or log(canvas.height)/5
        gap = canvas.line_width * border_ratio

        canvas.fill_style = color

        canvas.stroke_rect(pos_x, pos_y, rect_x, rect_y)
        canvas.fill_rect(pos_x, pos_y, rect_x, rect_y)
        canvas.stroke_rect(pos_x, pos_y, rect_x, rect_y)
        canvas.clear_rect(pos_x + gap, pos_y + gap, rect_x - 2 * gap,
                          rect_y - 2 * gap)
        canvas.stroke_rect(pos_x + gap, pos_y + gap, rect_x - 2 * gap,
                           rect_y - 2 * gap)

# Internal Cell
from PIL import Image as pilImage

# can we do this without reading image?
def get_image_size(path):
    pil_im = pilImage.open(path)
    return pil_im.width, pil_im.height

# Internal Cell

def draw_img(canvas, file, clear=False):
    # draws resized image on canvas and returns scale used
    with hold_canvas(canvas):
        if clear:
            canvas.clear()

        sprite1 = Image.from_file(file)

        width_canvas, height_canvas = canvas.width, canvas.height
        width_img, height_img = get_image_size(file)

        ratio_canvas = float(width_canvas) / height_canvas
        ratio_img = float(width_img) / height_img

        if ratio_img > ratio_canvas:
            # wider then canvas, scale to canvas width
            scale = width_canvas / width_img
        else:
            # taller then canvas, scale to canvas hight
            scale = height_canvas / height_img

        canvas.draw_image(sprite1, 0, 0,
                          width=width_img * min(1, scale),
                          height=height_img * min(1, scale))
        return scale

# Internal Cell

def points2bbox_coords(start_x, start_y, end_x, end_y):
    min_x, max_x = sorted((start_x, end_x))
    min_y, max_y = sorted((start_y, end_y))
    return {'x': min_x, 'y': min_y, 'width': max_x-min_x, 'height': max_y-min_y}


# Cell

class BBoxCanvas(HBox, traitlets.HasTraits):
    """
    Represents canvas holding image and bbox ontop.
    Gives user an ability to draw a bbox with mouse.

    """
    debug_output = widgets.Output(layout={'border': '1px solid black'})
    image_path = traitlets.Unicode()
    bbox_coords = traitlets.Dict()
    _canvas_bbox_coords = traitlets.Dict()
    _image_scale = traitlets.Float()

    def __init__(self, width, height):
        super().__init__()

        self.is_drawing = False
        self._start_point = ()
        self._image_scale = 1.0

        self._bg_layer = 0
        self._image_layer = 1
        self._box_layer = 2
        # do not stick bbox to borders
        self.padding = 2

        # Define each of the children...
        self._image = Image(layout=Layout(display='flex',
                                          justify_content='center',
                                          align_items='center',
                                          align_content='center'))
        self._multi_canvas = MultiCanvas(3, width=width, height=height)
        self._im_name_box = Label()

        children = [VBox([self._multi_canvas, self._im_name_box])]
        self.children = children
        draw_bg(self._multi_canvas[self._bg_layer])

        # link drawing events
        self._multi_canvas[self._box_layer].on_mouse_move(self._update_pos)
        self._multi_canvas[self._box_layer].on_mouse_down(self._start_drawing)
        self._multi_canvas[self._box_layer].on_mouse_up(self._stop_drawing)


    @debug_output.capture(clear_output=False)
    def _update_pos(self, x, y):
        if self.is_drawing:
            self._canvas_bbox_coords = points2bbox_coords(*self._start_point, x, y)
            # bbox should not cross the canvas border:
            if self._invalid_coords(x, y):
                print(' !! Out of canvas border !!')
                self._stop_drawing(x, y)

    def _invalid_coords(self, x, y):
        return (self._canvas_bbox_coords["x"] + self._canvas_bbox_coords["width"] > self._multi_canvas.width - self.padding or
                self._canvas_bbox_coords["y"] + self._canvas_bbox_coords["height"] > self._multi_canvas.height - self.padding or
                self._canvas_bbox_coords["x"] < self.padding or
                self._canvas_bbox_coords["y"] < self.padding)


    @debug_output.capture(clear_output=True)
    def _start_drawing(self, x, y):
#         print("-> START DRAWING")
        self._start_point = (x, y)
        self.is_drawing = True
#         print("<- START DRAWING")

    @debug_output.capture(clear_output=False)
    def _stop_drawing(self, x, y):
#         print("-> STOP DRAWING")
        self.is_drawing = False

        # if something is drawn
        if self._canvas_bbox_coords:
            # if bbox is not human visible, clean:
            if (self._canvas_bbox_coords['width'] < 10 or
                self._canvas_bbox_coords['height'] < 10):
                self._canvas_bbox_coords = {}
                print(" !! too small bbox drawn !!")
            else: # otherwise, save bbox values to backend
                self.bbox_coords = dict({ k: v / self._image_scale for k, v in self._canvas_bbox_coords.items() })
#         print("<- STOP DRAWING")


    @traitlets.observe('bbox_coords')
    def _update_canvas_bbox_coords(self, change):
#         print('-> Observe bbox_coords: ', change)

        if change['new'] == self._canvas_bbox_coords: # change event from gui, do nothing
            pass
#             print('-> GUI')
        else: # recalculate canvas coordinates as bbox was set by backend:
            self._canvas_bbox_coords = {k: v * self._image_scale for k, v in self.bbox_coords.items()}
#             print('-> Backend')
#         print('<- Observe bbox_coords')


    @traitlets.observe('_canvas_bbox_coords')
    def _draw_bbox(self, change):
#         print('-> Observe canvas_coords: ', change)
        if not self._canvas_bbox_coords:
            self._clear_bbox()
            self.bbox_coords = {}
            return
        coords = [self._canvas_bbox_coords['x'],
                  self._canvas_bbox_coords['y'],
                  self._canvas_bbox_coords['width'],
                  self._canvas_bbox_coords['height']]
        draw_bounding_box(self._multi_canvas[self._box_layer], coords,
                          color='white', border_ratio=2, clear=True)
#         print('<- Observe canvas_coords')


    def _clear_bbox(self):
        self._multi_canvas[self._box_layer].clear()


    @traitlets.observe('image_path')
    def _draw_image(self, image):
        self._image_scale = draw_img(self._multi_canvas[self._image_layer], self.image_path, clear=True)
        self._im_name_box.value = Path(self.image_path).name

    @property
    def image_scale(self):
        return self._image_scale

    def _clear_image(self):
        self._multi_canvas[self._image_layer].clear()

    # needed to support voila
    # https://ipycanvas.readthedocs.io/en/latest/advanced.html#ipycanvas-in-voila
    def observe_client_ready(self, cb=None):
        self._multi_canvas.on_client_ready(cb)