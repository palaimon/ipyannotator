# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/04_multi_bbox_annotator.ipynb (unless otherwise specified).

__all__ = ['BBoxAnnotator', 'MultiBBoxAnnotator']

# Internal Cell

import os
import json

from ipyevents import Event
from ipywidgets import (AppLayout, Button, IntSlider, IntProgress,
                        HBox, VBox, Output,
                        Layout, Label)
from pathlib import Path
from traitlets import Int, observe, link, dlink, HasTraits, Bytes, Unicode, Dict

from .bbox_canvas import BBoxCanvas
from .navi_widget import Navi
from .storage import setup_project_paths, get_image_list_from_folder, AnnotationStorage

# Internal Cell

class BBoxAnnotatorGUI(AppLayout):

    def __init__(self, canvas_size=(505, 50)):
        self._navi = Navi()

        self._save_btn = Button(description="Save",
                                layout=Layout(width='auto'))

        self._controls_box = HBox([self._navi, self._save_btn],
                                 layout=Layout(display='flex', flex_flow='row wrap', align_items='center'))

        self._image_box = BBoxCanvas(*canvas_size)

        super().__init__(header=None,
                 left_sidebar=None,
                 center=self._image_box,
                 right_sidebar=None,
                 footer=self._controls_box,
                 pane_widths=(2, 8, 0),
                 pane_heights=(1, 4, 1))


    def on_client_ready(self, callback):
        self._image_box.observe_client_ready(callback)

# Internal Cell

class BBoxAnnotatorLogic(HasTraits):
    index = Int(0)
    image_path = Unicode()
    bbox_coords = Dict()
    current_im_num = Int()

    def __init__(self, project_path, file_name=None, image_dir='pics', results_dir=None):
        self.project_path = Path(project_path)
        self.image_dir, self.annotation_file_path = setup_project_paths(self.project_path,
                                                                        file_name=file_name,
                                                                        image_dir=image_dir,
                                                                        results_dir=results_dir)

        # select images and bboxes only from given annotatin file
        if self.annotation_file_path.is_file():
            with self.annotation_file_path.open() as json_file:
                data = json.load(json_file)
                im_names = data.keys()
            self.image_paths = sorted(im for im in get_image_list_from_folder(self.image_dir) if str(im) in im_names)
        else:
            self.image_paths = sorted(get_image_list_from_folder(self.image_dir))


        if not self.image_paths:
            raise Exception ("!! No Images to dipslay !!")

        self.current_im_num = len(self.image_paths)

        self.annotations = AnnotationStorage(self.image_paths)

        if self.annotation_file_path.exists():
            self.annotations.load(self.annotation_file_path)
        else:
            self.annotations.save(self.annotation_file_path)

    def _update_im(self):
        self.image_path = str(self.image_paths[self.index])

    def _update_coords(self): # from annotations
        self.bbox_coords = self.annotations.get(self.image_path) or {}

    def _update_annotations(self, index): # from coordinates
        self.annotations[str(self.image_paths[index])] = self.bbox_coords

    def _save_annotations(self, *args, **kwargs): # to disk
        index = kwargs.pop('old_index', self.index)
        self._update_annotations(index)
        self.annotations.save(self.annotation_file_path)

    def _handle_client_ready(self):
        self._update_im()
        self._update_coords()

    @observe('index')
    def _idx_changed(self, change):
        ''' On index change save an old state
            and update current image path and bbox coordinates for visualisation
        '''
        self._save_annotations(old_index = change['old'])

        self._update_im()
        self._update_coords()

# Cell

class BBoxAnnotator(BBoxAnnotatorGUI):
    """
    Represents bounding box annotator.

    Gives an ability to itarate through image dataset,
    draw 2D bounding box annotations for object detection and localization,
    export final annotations in json format

    """
    debug_output = Output()

    def __init__(self, project_path, canvas_size=(200, 400), file_name=None, image_dir='pics', results_dir=None):
        self._model = BBoxAnnotatorLogic(project_path, file_name=file_name,
                                         image_dir=image_dir, results_dir=results_dir)

        super().__init__(canvas_size=canvas_size)

        self._save_btn.on_click(self._model._save_annotations)

        # set correct slider max value based on image number
        dlink((self._model, 'current_im_num'), (self._navi.model, 'max_im_number'))

        # draw current image and bbox only when client is ready
        self.on_client_ready(self._model._handle_client_ready)

        # Link image path and bbox coordinates between model and the ImageWithBox widget
        link((self._model, 'image_path'), (self._image_box, 'image_path'))
        link((self._model, 'bbox_coords'), (self._image_box, 'bbox_coords'))

        # Link current image index from controls to annotator model
        link((self._navi.model, 'index'), (self._model, 'index'))

    def to_dict(self, only_annotated=True):
        return self._model.annotations.to_dict(only_annotated)


# Internal Cell

import os
import json

from ipyevents import Event
from ipywidgets import (AppLayout, Button, IntSlider, IntProgress,
                        HBox, VBox, Output,
                        Layout, Label)
from pathlib import Path
from traitlets import Int, observe, link, dlink, HasTraits, Bytes, Unicode, Dict

from .bbox_canvas import BBoxCanvas, MultiBBoxCanvas
from .navi_widget import Navi
from .storage import setup_project_paths, get_image_list_from_folder, AnnotationStorage

# Internal Cell

class MultiBBoxAnnotatorGUI(AppLayout):

    def __init__(self, canvas_size=(505, 50)):
        self._navi = Navi()

        self._save_btn = Button(description="Save",
                                layout=Layout(width='auto'))

        self._clear_all_btn = Button(description="Clear all",
                                layout=Layout(width='auto'))

        self._clear_last_btn = Button(description="Clear last",
                                layout=Layout(width='auto'))

        self._controls_box = HBox([self._navi, self._clear_last_btn, self._clear_all_btn, self._save_btn],
                                 layout=Layout(display='flex', flex_flow='row wrap', align_items='center'))

        self._image_box = MultiBBoxCanvas(*canvas_size)

        super().__init__(header=None,
                 left_sidebar=None,
                 center=self._image_box,
                 right_sidebar=None,
                 footer=self._controls_box,
                 pane_widths=(2, 8, 0),
                 pane_heights=(1, 4, 1))

    def on_client_ready(self, callback):
        self._image_box.observe_client_ready(callback)

# Internal Cell

class MultiBBoxAnnotatorLogic(HasTraits):
    index = Int(0)
    image_path = Unicode()
    bbox_coords = Dict()
    current_im_num = Int()
    _bbox_index = Int()

    def __init__(self, project_path, file_name=None, image_dir='pics', results_dir=None):
        self.project_path = Path(project_path)
        self.image_dir, self.annotation_file_path = setup_project_paths(self.project_path,
                                                                        file_name=file_name,
                                                                        image_dir=image_dir,
                                                                        results_dir=results_dir)

        # select images and bboxes only from given annotation file
        if self.annotation_file_path.is_file():
            with self.annotation_file_path.open() as json_file:
                data = json.load(json_file)
                im_names = data.keys()
            self.image_paths = sorted(im for im in get_image_list_from_folder(self.image_dir) if str(im) in im_names)
        else:
            self.image_paths = sorted(get_image_list_from_folder(self.image_dir))

        if not self.image_paths:
            raise Exception ("!! No Images to display !!")

        self.current_im_num = len(self.image_paths)

        self.annotations = AnnotationStorage(self.image_paths)

        if self.annotation_file_path.exists():
            self.annotations.load(self.annotation_file_path)
        else:
            self.annotations.save(self.annotation_file_path)

    def _update_im(self):
        self.image_path = str(self.image_paths[self.index])

    def _update_coords(self): # from annotations
        tmp_coords = self.annotations.get(self.image_path) or {}
        # As bbox index are saved as str, we transform them into int
        if tmp_coords:
            tmp_coords = {int(k): v for k, v in tmp_coords.items()}
        self.bbox_coords = tmp_coords


    def _update_annotations(self, index): # from coordinates
        self.annotations[str(self.image_paths[index])] = self.bbox_coords

    def _save_annotations(self, *args, **kwargs): # to disk
        index = kwargs.pop('old_index', self.index)
        self._update_annotations(index)
        self.annotations.save(self.annotation_file_path)

    def _handle_client_ready(self):
        self._update_im()
        self._update_coords()

    @observe('index')
    def _idx_changed(self, change):
        ''' On index change save an old state
            and update current image path and bbox coordinates for visualisation
        '''
        self._save_annotations(old_index = change['old'])

        self._update_im()
        self._update_coords()

# Cell

class MultiBBoxAnnotator(MultiBBoxAnnotatorGUI):
    """
    Represents multi bounding box annotator.

    Gives an ability to itarate through image dataset,
    draw multiple 2D bounding box annotations for object detection
    and localization, export final annotations in json format

    """
    debug_output = Output()

    def __init__(self, project_path, canvas_size=(200, 400), file_name=None, image_dir='pics', results_dir=None):
        self._model = MultiBBoxAnnotatorLogic(project_path, file_name=file_name,
                                              image_dir=image_dir, results_dir=results_dir)

        super().__init__(canvas_size=canvas_size)

        self._save_btn.on_click(self._model._save_annotations)

        self._clear_all_btn.on_click(self._on_clear_all)

        self._clear_last_btn.on_click(self._on_clear_last)

        # set correct slider max value based on image number
        dlink((self._model, 'current_im_num'), (self._navi.model, 'max_im_number'))

        # draw current image and bbox only when client is ready
        self.on_client_ready(self._model._handle_client_ready)

        # Link image path and bbox coordinates between model and the ImageWithBox widget
        link((self._model, 'image_path'), (self._image_box, 'image_path'))
        link((self._model, 'bbox_coords'), (self._image_box, 'bbox_coords'))

        # Link current image index from controls to annotator model
        link((self._navi.model, 'index'), (self._model, 'index'))

    def to_dict(self, only_annotated=True):
        return self._model.annotations.to_dict(only_annotated)

    def _on_clear_all(self, arg):
        self._image_box.clear_all_bbox()

    def _on_clear_last(self, arg):
        self._image_box.clear_last_bbox()
