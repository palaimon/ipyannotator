# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01_bbox_canvas.ipynb (unless otherwise specified).

__all__ = ['points2bbox_coords', 'coords_scaled', 'BBoxCanvas', 'BBoxVideoCanvas']

# Internal Cell
import io
import attr
from math import log
from pubsub import pub
from attr import asdict
from pathlib import Path
from copy import deepcopy
from enum import IntEnum
from typing import Dict, Optional, List, Any, Tuple

from abc import ABC, abstractmethod
from pydantic import root_validator
from .base import BaseState
from .docs.utils import is_building_docs
from .mltypes import BboxCoordinate, BboxVideoCoordinate
from ipycanvas import MultiCanvas as IMultiCanvas, Canvas, hold_canvas
from ipywidgets import Image, Label, Layout, HBox, VBox, Output
from PIL import Image as PILImage

# Internal Cell
if not is_building_docs():
    class MultiCanvas(IMultiCanvas):
        pass
else:
    class MultiCanvas(Image):  # type: ignore
        def __init__(self, *args, **kwargs):
            super().__init__(**kwargs)
            image = PILImage.new('RGB', (100, 100), (255, 255, 255))
            b = io.BytesIO()
            image.save(b, format='PNG')
            self.value = b.getvalue()

        def __getitem__(self, key):
            return self

        def draw_image(self, image, x=0, y=0, width=None, height=None):
            self.value = image.value
            self.width = width
            self.height = height

        def __getattr__(self, name):
            ignored = [
                'flush',
                'fill_rect',
                'stroke_rect',
                'stroke_rects',
                'on_mouse_move',
                'on_mouse_down',
                'on_mouse_up',
                'clear',
                'on_client_ready',
                'stroke_styled_line_segments'
            ]

            if name in ignored:
                def wrapper(*args, **kwargs):
                    return self._ignored(*args, **kwargs)
                return wrapper
            return object.__getattr__(self, name)

        @property
        def caching(self):
            return False

        @caching.setter
        def caching(self, value):
            pass

        @property
        def size(self):
            return (self.width, self.height)

        def _ignored(self, *args, **kwargs):
            pass

# Internal Cell
def draw_bg(canvas, color='rgb(236,240,241)'):
    with hold_canvas(canvas):
        canvas.fill_style = color
        canvas.fill_rect(0, 0, canvas.size[0], canvas.size[1])

# Internal Cell
def draw_bounding_box(canvas, coord: BboxCoordinate, color='white', line_width=1,
                      border_ratio=2, clear=False, stroke_color='black'):
    with hold_canvas(canvas):
        if clear:
            canvas.clear()

        line_width = line_width or log(canvas.height) / 5

        gap = line_width * border_ratio

        # paint and draw the middle stroked rectangle
        canvas.line_width = gap
        canvas.stroke_style = color
        canvas.stroke_rect(coord.x + gap / 2, coord.y + gap / 2,
                           coord.width - gap, coord.height - gap)

        # paint and draw the external stroked rectangle
        canvas.line_width = line_width
        canvas.stroke_style = stroke_color
        canvas.stroke_rect(coord.x, coord.y, coord.width, coord.height)

        # paint and draw the internal stroked rectangle
        canvas.line_width = line_width
        canvas.stroke_style = stroke_color
        canvas.stroke_rect(coord.x + gap, coord.y + gap,
                           coord.width - 2 * gap, coord.height - 2 * gap)

# Internal Cell
class BoundingBox:
    def __init__(self):
        self.color = 'white'
        self.line_width = 1
        self.border_ratio = 2
        self.stroke_color = 'black'

    def _empty_bbox(self) -> Dict[str, List[int]]:
        return {'x': [], 'y': [], 'width': [], 'height': []}

    def _stroke_rects(self, canvas: Canvas, bbox: Dict[str, List[int]],
                      line_width: float, color: str):
        canvas.line_width = line_width
        canvas.stroke_style = color
        canvas.stroke_rects(bbox['x'], bbox['y'], bbox['width'], bbox['height'])

    def draw(self, canvas: Canvas, coords: List[BboxCoordinate], clear: bool = False):
        with hold_canvas(canvas):
            if clear:
                canvas.clear()

            mid_rect = self._empty_bbox()
            inter_rect = self._empty_bbox()
            ext_rect = self._empty_bbox()

            line_width = self.line_width or log(canvas.height) / 5

            gap = line_width * self.border_ratio

            for coord in coords:
                mid_rect['x'].append(coord.x + gap / 2)
                mid_rect['y'].append(coord.y + gap / 2)
                mid_rect['width'].append(coord.width - gap)
                mid_rect['height'].append(coord.height - gap)

                ext_rect['x'].append(coord.x)
                ext_rect['y'].append(coord.y)
                ext_rect['width'].append(coord.width)
                ext_rect['height'].append(coord.height)

                inter_rect['x'].append(coord.x + gap)
                inter_rect['y'].append(coord.y + gap)
                inter_rect['width'].append(coord.width - 2 * gap)
                inter_rect['height'].append(coord.height - 2 * gap)

            # paint and draw the middle stroked rectangle
            self._stroke_rects(canvas, mid_rect, gap, self.color)

            # paint and draw the external stroked rectangle
            self._stroke_rects(canvas, ext_rect, line_width, self.stroke_color)

            # paint and draw the internal stroked rectangle
            self._stroke_rects(canvas, inter_rect, line_width, self.stroke_color)

# Internal Cell
from PIL import Image as pilImage


# can we do this without reading image?
def get_image_size(path):
    pil_im = pilImage.open(path)
    return pil_im.width, pil_im.height

# Internal Cell
@attr.define
class ImageCanvas:
    image_widget: Image
    x: int
    y: int
    width: int
    height: int
    scale: float

# Internal Cell
class ImageCanvasPrototype(ABC):
    @abstractmethod
    def prepare_canvas(self, canvas: Canvas, file: str) -> ImageCanvas:
        pass

# Internal Cell
class CanvasScaleMixin:
    def _calc_scale(
        self,
        width_canvas: int,
        height_canvas: int,
        width_img: float,
        height_img: float
    ) -> float:
        ratio_canvas = float(width_canvas) / height_canvas
        ratio_img = float(width_img) / height_img

        if ratio_img > ratio_canvas:
            # wider then canvas, scale to canvas width
            return width_canvas / width_img

        # taller then canvas, scale to canvas height
        return height_canvas / height_img

# Internal Cell
class ScaledImage(ImageCanvasPrototype, CanvasScaleMixin):
    def prepare_canvas(self, canvas: Canvas, file: str) -> ImageCanvas:
        image = Image.from_file(file)
        width_img, height_img = get_image_size(file)

        scale = self._calc_scale(
            int(canvas.width),
            int(canvas.height),
            width_img,
            height_img
        )

        image_width = width_img * min(1, scale)
        image_height = height_img * min(1, scale)

        return ImageCanvas(
            image_widget=image,
            x=0,
            y=0,
            width=image_width,
            height=image_height,
            scale=scale
        )

# Internal Cell
class FitImage(ImageCanvasPrototype):
    def prepare_canvas(self, canvas: Canvas, file: str) -> ImageCanvas:
        image = Image.from_file(file)

        return ImageCanvas(
            image_widget=image,
            x=0,
            y=0,
            width=canvas.width,
            height=canvas.height,
            scale=1
        )

# Internal Cell
class ImageRenderer:
    def __init__(
        self,
        clear: bool = False,
        has_border: bool = False,
        fit_canvas: bool = False
    ):
        self.clear = clear
        self.has_border = has_border
        self.fit_canvas = fit_canvas
        if fit_canvas:
            self._strategy = FitImage()  # type: ImageCanvasPrototype
        else:
            self._strategy = ScaledImage()

    def render(self, canvas: Canvas, file: str) -> Tuple[int, int, float]:
        with hold_canvas(canvas):
            if self.clear:
                canvas.clear()

            image_canvas = self._strategy.prepare_canvas(canvas, file)

            if self.has_border:
                canvas.stroke_rect(x=0, y=0, width=image_canvas.width, height=image_canvas.height)
                image_canvas.width -= 2
                image_canvas.height -= 2
                image_canvas.x, image_canvas.y = 1, 1

            canvas.draw_image(
                image_canvas.image_widget,
                image_canvas.x,
                image_canvas.y,
                image_canvas.width,
                image_canvas.height
            )

            return image_canvas.width, image_canvas.height, image_canvas.scale

# Cell

def points2bbox_coords(start_x, start_y, end_x, end_y) -> Dict[str, float]:
    min_x, max_x = sorted((start_x, end_x))
    min_y, max_y = sorted((start_y, end_y))
    return {'x': min_x, 'y': min_y, 'width': max_x - min_x, 'height': max_y - min_y}

# Cell
def coords_scaled(bbox_coords: List[float], image_scale: float):
    return [value * image_scale for value in bbox_coords]

# Internal Cell

class BBoxLayer(IntEnum):
    bg = 0
    image = 1
    box = 2
    highlight = 3
    drawing = 4

# Internal Cell

class BBoxCanvasState(BaseState):
    image_path: Optional[str]
    bbox_coords: List[BboxCoordinate] = []
    image_scale: float = 1
    image_height: Optional[int] = None
    image_width: Optional[int] = None
    bbox_selected: Optional[int]
    height: Optional[int]
    width: Optional[int]
    fit_canvas: bool = False

    @root_validator
    def set_height(cls, values):
        if not values.get('image_height'):
            values['image_height'] = values.get('height')

        if not values.get('image_width'):
            values['image_width'] = values.get('width')

        return values

# Internal Cell

class BBoxCanvasGUI(HBox):
    debug_output = Output(layout={'border': '1px solid black'})

    def __init__(
        self,
        state: BBoxCanvasState,
        has_border: bool = False,
        drawing_enabled: bool = True
    ):
        super().__init__()

        self._state = state
        self._start_point = ()
        self.is_drawing = False
        self.has_border = has_border
        self.canvas_bbox_coords: Dict[str, Any] = {}
        self.drawing_enabled = drawing_enabled

        # do not stick bbox to borders
        self.padding = 2

        # Define each of the children...
        self._image = Image(layout=Layout(display='flex',
                                          justify_content='center',
                                          align_items='center',
                                          align_content='center',
                                          overflow='hidden'))

        if not drawing_enabled:
            self.multi_canvas = MultiCanvas(
                len(BBoxLayer),
                width=self._state.width,
                height=self._state.height
            )
            self.children = [VBox([self.multi_canvas])]
        else:
            self.multi_canvas = MultiCanvas(
                len(BBoxLayer),
                width=self._state.width,
                height=self._state.height
            )

            self.im_name_box = Label()

            children = [VBox([self.multi_canvas, self.im_name_box])]
            self.children = children
            draw_bg(self.multi_canvas[BBoxLayer.bg])

            # link drawing events
            self.multi_canvas[BBoxLayer.drawing].on_mouse_move(self._update_pos)
            self.multi_canvas[BBoxLayer.drawing].on_mouse_down(self._start_drawing)
            self.multi_canvas[BBoxLayer.drawing].on_mouse_up(self._stop_drawing)

    @property
    def highlight(self) -> BboxCoordinate:
        return self._state.bbox_coords[self.bbox_selected]

    @highlight.setter
    def highlight(self, index: int):
        self.clear_layer(BBoxLayer.highlight)

        # unhighlight when double click
        if self._state.bbox_coords and self._state.bbox_selected == index:
            self._state.set_quietly('bbox_selected', None)
            return
        _bbox_coords = list(asdict(self._state.bbox_coords[index]).values())
        _bbox_coords_scaled = coords_scaled(_bbox_coords,
                                            self._state.image_scale)
        bbox_coords = BboxCoordinate(*_bbox_coords_scaled)

        draw_bounding_box(
            self.multi_canvas[BBoxLayer.highlight],
            bbox_coords,
            stroke_color='black',
            border_ratio=3,
            color='yellow'
        )

        self._state.set_quietly('bbox_selected', index)

    @debug_output.capture(clear_output=True)
    def _update_pos(self, x, y):
        # print(f"-> BBoxCanvasGUI::_update_post({x}, {y})")
        if self.is_drawing:
            self.canvas_bbox_coords = points2bbox_coords(*self._start_point, x, y)
            self.draw_bbox(self.canvas_bbox_coords)
            # bbox should not cross the canvas border:
            if self._invalid_coords(x, y):
                print(' !! Out of canvas border !!')
                self._stop_drawing(x, y)
        # print(f"<- BBoxCanvasGUI::_update_post({x}, {y})")

    def _invalid_coords(self, x, y) -> bool:
        return (
            self.canvas_bbox_coords["x"] + self.canvas_bbox_coords["width"] >
            self.multi_canvas.width - self.padding or
            self.canvas_bbox_coords["y"] + self.canvas_bbox_coords["height"] >
            self.multi_canvas.height - self.padding or
            self.canvas_bbox_coords["x"] < self.padding or
            self.canvas_bbox_coords["y"] < self.padding)

    @debug_output.capture(clear_output=True)
    def _stop_drawing(self, x, y):
        # print(f"-> BBoxCanvasGUI::_stop_drawing({x}, {y})")
        self.is_drawing = False

        # if something is drawn
        if self.canvas_bbox_coords:
            # if bbox is not human visible, clean:
            if (self.canvas_bbox_coords['width'] < 10 or
                    self.canvas_bbox_coords['height'] < 10):
                self.clear_layer(BBoxLayer.drawing)
                print(" !! too small bbox drawn !!")
            else:  # otherwise, save bbox values to backend
                tmp_bbox_coords = deepcopy(self._state.bbox_coords)
                tmp_bbox_coords.append(
                    BboxCoordinate(
                        **{k: v / self._state.image_scale for k, v in self.canvas_bbox_coords.items()}  # noqa: E501
                    )
                )
                self._state.bbox_coords = tmp_bbox_coords
            self.canvas_bbox_coords = {}
        # print(f"<- BBoxCanvasGUI::_stop_drawing({x}, {y})")

    def draw_bbox(self, canvas_bbox_coords: dict, color='white'):
        # print('-> Observe canvas_coords: ', canvas_bbox_coords)
        if not canvas_bbox_coords:
            self.clear_layer(BBoxLayer.box)
            self._state.bbox_coords = []
            return

        coords = BboxCoordinate(*canvas_bbox_coords.values())

        draw_bounding_box(
            self.multi_canvas[BBoxLayer.drawing],
            coords,
            color='white',
            border_ratio=2,
            clear=True
        )
        # print('<- Observe canvas_coords')

    def clear_layer(self, layer: int):
        self.multi_canvas[layer].clear()

    @debug_output.capture(clear_output=True)
    def _start_drawing(self, x, y):
        # print(f"-> BBoxCanvasGUI::_start_drawing({x}, {y})")
        self._start_point = (x, y)
        self.is_drawing = True
        # print(f"<- BBoxCanvasGUI::_start_drawing({x}, {y})")

    # needed to support voila
    # https://ipycanvas.readthedocs.io/en/latest/advanced.html#ipycanvas-in-voila
    def observe_client_ready(self, cb=None):
        self.multi_canvas.on_client_ready(cb)

# Internal Cell

class BBoxVideoCanvasGUI(BBoxCanvasGUI):
    debug_output = Output(layout={'border': '1px solid black'})

    def __init__(
        self,
        state: BBoxCanvasState,
        has_border: bool = False,
        drawing_enabled: bool = True
    ):
        super().__init__(state, has_border, drawing_enabled)

    @property
    def highlight(self) -> BboxCoordinate:
        return self._state.bbox_coords[self.bbox_selected]

    @highlight.setter
    def highlight(self, index: int):
        self.clear_layer(BBoxLayer.highlight)

        # unhighlight when double click
        if self._state.bbox_coords and self._state.bbox_selected == index:
            self._state.set_quietly('bbox_selected', None)
            return

        _bbox_coords = list(asdict(self._state.bbox_coords[index]).values())
        _bbox_coords_scaled = coords_scaled(
            _bbox_coords[:4], self._state.image_scale)
        bbox_coords = BboxCoordinate(*_bbox_coords_scaled)

        draw_bounding_box(
            self.multi_canvas[BBoxLayer.highlight],
            bbox_coords,
            stroke_color='black',
            border_ratio=3,
            color='yellow'
        )

        self._state.set_quietly('bbox_selected', index)

    @debug_output.capture(clear_output=False)
    def _stop_drawing(self, x, y):
        #print(f"-> BBoxVideoCanvasGUI::_stop_drawing({x}, {y})")
        self.is_drawing = False

        # if something is drawn
        if self.canvas_bbox_coords:
            # if bbox is not human visible, clean:
            if (self.canvas_bbox_coords['width'] < 10 or
                    self.canvas_bbox_coords['height'] < 10):
                self.clear_layer(BBoxLayer.drawing)
                print(" !! too small bbox drawn !!")
            else:  # otherwise, save bbox values to backend
                tmp_bbox_coords = deepcopy(self._state.bbox_coords)
                tmp_bbox_coords.append(
                    BboxVideoCoordinate(**{
                        **{k: v / self._state.image_scale for k, v in self.canvas_bbox_coords.items()},  # noqa: E501
                        **{'id': str(len(self._state.bbox_coords))}  # TODO::improve id generation
                    })
                )
                self._state.bbox_coords = tmp_bbox_coords
            self.canvas_bbox_coords = {}
        # print(f"<- BBoxVideoCanvasGUI::_stop_drawing({x}, {y})")

    @debug_output.capture(clear_output=False)
    def draw_bbox(self, canvas_bbox_coords: dict, color='white'):
        # print('-> Observe canvas_coords: ', canvas_bbox_coords)
        if not canvas_bbox_coords:
            self.clear_layer(BBoxLayer.box)
            self._state.set_quietly('bbox_coords', [])
            return

        coords = BboxCoordinate(*list(canvas_bbox_coords.values())[:4])

        draw_bounding_box(
            self.multi_canvas[BBoxLayer.drawing],
            coords,
            color='white',
            border_ratio=2,
            clear=True
        )

# Internal Cell

class BBoxCanvasController:
    """
    Handle the GUI and state communication
    """
    debug_output = Output(layout={'border': '1px solid black'})

    def __init__(self, gui: BBoxCanvasGUI, state: BBoxCanvasState):
        self._state = state
        self._gui = gui

        state.subscribe(self._draw_all_bbox, 'bbox_coords')
        state.subscribe(self._draw_image, 'image_path')
        pub.subscribe(self._draw_all_bbox, f'{state.root_topic}.coord_changed')
        self.bbox = BoundingBox()

    @debug_output.capture(clear_output=True)
    def _draw_all_bbox(self, bbox_coords: List[BboxCoordinate]):
        # print(f"-> BBoxCanvasController::_draw_all_bbox: {bbox_coords}")
        self._gui.clear_layer(BBoxLayer.box)
        self._gui.clear_layer(BBoxLayer.highlight)
        self._gui.clear_layer(BBoxLayer.drawing)

        all_bbox = []
        for bbox_coord in bbox_coords:
            coord = list(asdict(bbox_coord).values())
            coord = coords_scaled(coord, self._state.image_scale)
            all_bbox.append(BboxCoordinate(*coord))

        self.bbox.draw(
            canvas=self._gui.multi_canvas[BBoxLayer.box],
            coords=all_bbox,
            clear=False
        )
        # print(f"<- BBoxCanvasController::_draw_all_bbox")

    def clear_all_bbox(self):
        self._gui.clear_layer(BBoxLayer.box)
        self._gui.clear_layer(BBoxLayer.highlight)
        self._gui.clear_layer(BBoxLayer.drawing)
        self._state.set_quietly('bbox_coords', [])

    @debug_output.capture(clear_output=True)
    def _draw_image(self, image_path: str):
        print(f"-> _draw_image {image_path}")
        self.clear_all_bbox()

        img_renderer_service = ImageRenderer(
            clear=True,
            has_border=self._gui.has_border,
            fit_canvas=self._state.fit_canvas
        )

        image_width, image_height, scale = img_renderer_service.render(
            self._gui.multi_canvas[BBoxLayer.image],
            image_path
        )

        self._state.set_quietly('image_width', image_width)
        self._state.set_quietly('image_height', image_height)
        self._state.image_scale = scale
        self._gui.im_name_box.value = Path(image_path).name
        # print(f"<- _draw_image {image_path}")

# Internal Cell

class BBoxVideoCanvasController(BBoxCanvasController):
    debug_output = Output(layout={'border': '1px solid black'})

    def __init__(self, gui: BBoxCanvasGUI, state: BBoxCanvasState):
        super().__init__(gui, state)

    @debug_output.capture(clear_output=True)
    def _draw_all_bbox(self, bbox_coords: List[BboxVideoCoordinate]):
        #print(f"-> BBoxVideoCanvasController::_draw_all_bbox: {bbox_coords}")
        self._gui.clear_layer(BBoxLayer.box)
        self._gui.clear_layer(BBoxLayer.highlight)
        self._gui.clear_layer(BBoxLayer.drawing)

        all_bbox = []
        for bbox_coord in bbox_coords:
            coord = list(asdict(bbox_coord).values())[:4]
            coord = coords_scaled(coord, self._state.image_scale)
            all_bbox.append(BboxCoordinate(*coord))

        self.bbox.draw(
            canvas=self._gui.multi_canvas[BBoxLayer.box],
            coords=all_bbox,
            clear=False
        )

# Cell

class BBoxCanvas(BBoxCanvasGUI):
    """
    Represents canvas holding image and bbox ontop.
    Gives user an ability to draw a bbox with mouse.
    """

    def __init__(
        self,
        width,
        height,
        has_border: bool = False,
        fit_canvas: bool = False,
        drawing_enabled: bool = True
    ):
        self.state = BBoxCanvasState(
            uuid=str(id(self)),
            **{'width': width, 'height': height, 'fit_canvas': fit_canvas}
        )
        super().__init__(
            state=self.state,
            has_border=has_border,
            drawing_enabled=drawing_enabled
        )
        self._controller = BBoxCanvasController(gui=self, state=self.state)
        self._bbox_history: List[Any] = []

    def undo_bbox(self):
        if self.state.bbox_coords:
            tmp_bbox_coords = deepcopy(self.state.bbox_coords)
            removed_bbox = tmp_bbox_coords.pop()
            self._bbox_history = [removed_bbox]
            self.state.bbox_coords = tmp_bbox_coords

    def redo_bbox(self):
        if self._bbox_history:
            tmp_bbox_coords = deepcopy(self.state.bbox_coords)
            tmp_bbox_coords.append(self._bbox_history.pop())
            self.state.bbox_coords = tmp_bbox_coords

    def clear_all_bbox(self):
        self._controller.clear_all_bbox()

    def observe_client_ready(self, cb=None):
        self.multi_canvas.on_client_ready(cb)

# Cell

class BBoxVideoCanvas(BBoxVideoCanvasGUI):
    def __init__(self, width, height, has_border: bool = False, drawing_enabled: bool = True):
        self.state = BBoxCanvasState(
            uuid=str(id(self)),
            **{'width': width, 'height': height}
        )
        self.drawing_enabled = drawing_enabled
        super().__init__(state=self.state, has_border=has_border, drawing_enabled=drawing_enabled)

        self._controller = BBoxVideoCanvasController(gui=self, state=self.state)