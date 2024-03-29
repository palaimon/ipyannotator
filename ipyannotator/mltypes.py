# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00b_mltypes.ipynb (unless otherwise specified).

__all__ = ['Coordinate', 'BboxCoordinate', 'BboxVideoCoordinate', 'Input', 'Output', 'InputImage', 'OutputImageLabel',
           'OutputLabel', 'OutputImageBbox', 'OutputVideoBbox', 'OutputGridBox', 'NoOutput']

# Internal Cell
import warnings
import random
import uuid
import attr
from typing import List

# Cell
@attr.define(slots=False)
class Coordinate:
    x: int
    y: int


@attr.define(slots=False)
class BboxCoordinate(Coordinate):
    width: int
    height: int


@attr.define(slots=False)
class BboxVideoCoordinate(BboxCoordinate):
    id: str

    def bbox_coord(self) -> BboxCoordinate:
        return BboxCoordinate(*list(attr.asdict(self).values())[:4])

# Cell

# todo: use pydantic
class Input():
    """
    Abstract class to represent input
    """

    def __repr__(self):
        return f"Annotator Input type: {self.__class__.__name__}"


class Output():
    """
    Abstract class to represent input
    """

    def __repr__(self):
        return f"Annotator Output type: {self.__class__.__name__}"

# Cell
class InputImage(Input):
    """
    image_dir: string
        Directory of the image

    image_width: int
        Width of the image

    image_height: int
        Height of the image

    fit_canvas: bool
        Ignores the image size and fit image on the canvas size
    """

    def __init__(
        self,
        image_dir: str = 'pics',
        image_width: int = 100,
        image_height: int = 100,
        fit_canvas: bool = False
    ):
        self.width = image_width
        self.height = image_height
        self.dir = image_dir
        self.fit_canvas = fit_canvas

        if fit_canvas:
            warnings.warn("Image size will be ignored since fit_canvas is activated")

# Cell
class OutputImageLabel(Output):
    """
    Configures the image output.

    If no `label_dir` is specified, it generates randomized one.
    """

    def __init__(self, label_dir=None, label_width=50, label_height=50):
        self.width = label_width
        self.height = label_height

        if label_dir is None:
            self.dir = 'class_autogenerated_' + ''.join(random.sample(str(uuid.uuid4()), 5))
        else:
            self.dir = label_dir

# Cell
class OutputLabel(Output):
    def __init__(self, class_labels: List[str], label_width=50, label_height=50):
        self.width = label_width
        self.height = label_height
        self.class_labels = class_labels

# Cell
class OutputImageBbox(Output):
    """
    classes: List[str]
        Define the classes of objects available
        to be classified
    """

    def __init__(self, classes: List[str] = None):
        self.classes = classes or []
        self.drawing_enabled = True

# Cell
class OutputVideoBbox(OutputImageBbox):
    """
    Specialization of the OutputImageBbox.

    classes: List[str]
        Define the classes of objects available
        to be classified
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.drawing_enabled = True
        self.drawing_trajectory_enabled = True

# Cell
class OutputGridBox(Output):
    """Configures the capture annotator"""
    pass

# Cell
class NoOutput(Output):
    """Explore the data without worring
    about which type of data it's wanted
    to output"""
    pass