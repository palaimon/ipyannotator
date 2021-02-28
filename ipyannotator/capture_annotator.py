# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/06_capture_annotator.ipynb (unless otherwise specified).

__all__ = ['CaptureGrid', 'CaptureAnnotator']

# Internal Cell

from functools import partial
import math

from ipywidgets import (AppLayout, VBox, HBox, Button, GridBox, Layout, Checkbox, HTML, IntText, Valid, Output)
from ipyevents import Event

from pathlib import Path

from .navi_widget import Navi
from .storage import setup_project_paths, get_image_list_from_folder, AnnotationStorage

from traitlets import Dict, Int, HasTraits, observe, dlink, link, List, Unicode, Bool

from .image_button import ImageButton

# Cell

class CaptureGrid(GridBox, HasTraits):
    """
    Represents grid of `ImageButtons` with state.

    """
    debug_output = Output(layout={'border': '1px solid black'})
    current_state = Dict()

    def __init__(self, grid_item=ImageButton, image_width=150, image_height=150,
                 n_rows=3, n_cols=3, display_label=False):


        self.image_width = image_width
        self.image_height = image_height
        self.n_rows = n_rows
        self.n_cols = n_cols
        self._screen_im_number = IntText(value=n_rows * n_cols,
                                         description='screen_image_number',
                                         disabled=False)

        self._labels = [grid_item(display_label=display_label,
                                  image_width='%dpx' % self.image_width,
                                  image_height='%dpx' % self.image_height) for _ in range(self._screen_im_number.value)]

        self.callback = None

        self.observe(self.on_state_change, 'current_state')


        gap = 40 if display_label else 15

        centered_settings = {
            'grid_template_columns': " ".join(["%dpx" % (self.image_width + gap) for i
                                               in range(self.n_cols)]),
            'grid_template_rows': " ".join(["%dpx" % (self.image_height + gap) for i
                                            in range(self.n_rows)]),
            'justify_content': 'center',
            'align_content': 'space-around'
        }


        super().__init__(children=self._labels, layout=Layout(**centered_settings))


    @debug_output.capture(clear_output=True)
    def on_state_change(self, change=None):
        print('on_state_change', change['new'])
        new_state = change['new']
        updated = 0
        iter_state = iter(new_state)

        for label in self._labels:
            p = next(iter_state, None)
            if p:
                label.image_path = str(p)
                label.label_value = Path(p).stem
                label.active = new_state[p].get('answer', False)
            else:
                label.clear()

        if self.callback:
            self.register_on_click()


    def on_click(self, cb):
        self.callback = cb
        self.register_on_click()

    @debug_output.capture(clear_output=True)
    def register_on_click(self):
        print('register_on_click')
        for l in self._labels:
            l.reset_callbacks()
            l.on_click(partial(self.callback, name=l.name))

# Internal Cell

class CaptureAnnotatorGUI(AppLayout):
    def __init__(self, image_width=150, image_height=150,
                 n_rows=3, n_cols=3):

        self._screen_im_number = IntText(value=n_rows * n_cols,
                                    description='screen_image_number',
                                    disabled=False)

        self.image_width = image_width
        self.image_height = image_height
        self.n_rows = n_rows
        self.n_cols = n_cols

        self._navi = Navi()

        self._save_btn = Button(description="Save",
                                layout=Layout(width='auto'))

        self._none_checkbox = Checkbox(description="Select none",
                                       indent=False,
                                       layout=Layout(width='100px'))

        self._controls_box = HBox([self._navi, self._save_btn, self._none_checkbox],
                                 layout=Layout(display='flex', justify_content='center', flex_flow='wrap', align_items='center'))


        self._grid_box = CaptureGrid(image_width=image_width, image_height=image_height,  n_rows=n_rows, n_cols=n_cols, display_label=False)


        self._grid_label = HTML()
        self._labels_box = VBox(children = [self._grid_label, self._grid_box],
                                layout=Layout(display='flex', justify_content='center', flex_wrap='wrap', align_items='center'))


        super().__init__(header=None,
                 left_sidebar=None,
                 center=self._labels_box,
                 right_sidebar=None,
                 footer=self._controls_box,
                 pane_widths=(2, 8, 0),
                 pane_heights=(1, 4, 1))


# Internal Cell

class CaptureAnnotatorLogic(HasTraits):
    debug_output = Output(layout={'border': '1px solid black'})
    index = Int(0) # state index
    disp_number = Int() # number of images on screen
    num_screens = Int() # number of screens
    current_state = Dict()
    question_value = Unicode()
    all_none = Bool()


    def __init__(self, project_path, question=None, image_dir='pics', filter_files=None, results_dir=None):
        self.project_path = Path(project_path)
        self.image_dir, self.annotation_file_path = setup_project_paths(self.project_path, image_dir=image_dir, results_dir=results_dir)

        self.image_paths = sorted(get_image_list_from_folder(self.image_dir)) #todo: use sorted in storage?

        if filter_files:
            self.image_paths = [p for p in self.image_paths if str(p) in filter_files]
        if not self.image_paths:
            raise UserWarning("No image files to display! Check image_dir of filter.")
        self.current_im_num = len(self.image_paths)
        self.annotations = AnnotationStorage(self.image_paths)
        if question:
            self.question_value = f'<center><p style="font-size:20px;">{question}</p></center>'
        self._update_state()


    @observe('disp_number')
    def _update_state(self, change=None): # from annotations
        state_images = self._get_state_names(self.index)
        current_state = {}
        for im_path in state_images:
            current_state[str(im_path)] = self.annotations.get(str(im_path)) or {}
        self.all_none = all(value == {'answer': False} for value in current_state.values())
        self.current_state = current_state


    def _update_annotations(self, index): # from screen
        for p, anno in self.current_state.items():
            self.annotations[str(p)] = anno

    def _save_annotations(self, *args, **kwargs): # to disk
        index = kwargs.pop('old_index', self.index)
        self._update_annotations(index)
        self.annotations.save(self.annotation_file_path)

    def _get_state_names(self, index):
        start = index * self.disp_number
        end = start + self.disp_number
        im_names = self.image_paths[start:end]
        return im_names


    @observe('index')
    def _idx_changed(self, change):
        ''' On index change save old state
            and update current state for visualisation
        '''
        self._save_annotations(old_index = change['old'])
        # update new screen
        self._update_state()

    @observe('disp_number')
    def _calc_screens_num(self, change=None):
        self.num_screens = math.ceil(self.current_im_num / self.disp_number)


    @debug_output.capture(clear_output=False)
    def _handle_grid_click(self, event, name=None):
        p = Path(self.image_dir, name)
        current_state = self.current_state.copy()
        if not p.is_dir():
            current_state[str(p)] = {'answer': not self.current_state[str(p)].get('answer', False)}
            if self.all_none:
                self.all_none = False
        else:
            return
        self.current_state = current_state

    def _select_none(self, change=None):
        self.current_state = {p: {'answer': False} for p in self.current_state}

# Cell


class CaptureAnnotator(CaptureAnnotatorGUI):
    """
    Represents capture annotator.

    Gives an ability to itarate through image dataset,
    select images of same class,
    export final annotations in json format

    """

    def __init__(self, project_path, image_dir='pics', image_width=150, image_height=150,
                 n_rows=3, n_cols=3, question=None, filter_files=None, results_dir=None):

        super().__init__(image_width, image_height, n_rows, n_cols)

        self._model = CaptureAnnotatorLogic(project_path, question, image_dir,
                                           filter_files=filter_files, results_dir=results_dir)

        self._save_btn.on_click(self._model._save_annotations)

        self._grid_box.on_click(self._model._handle_grid_click)

        link((self._model, 'all_none'), (self._none_checkbox, 'value'))

        self._none_checkbox.observe(self._model._select_none, 'value')

        # get correct screen image number from gui settings
        dlink((self._screen_im_number, 'value'), (self._model, 'disp_number'))

        # set correct number of screens slider value based on image number
        dlink((self._model, 'num_screens'), (self._navi.model, 'max_im_number'))

        # link current image index from controls to annotator model
        link((self._navi.model, 'index'), (self._model, 'index'))

        # link annotation question
        link((self._model, 'question_value'), (self._grid_label, 'value'))

        # link state of model and grid box visualizer
        link((self._model, 'current_state'), (self._grid_box, 'current_state'))



    def to_dict(self, only_annotated=True):
        return self._model.annotations.to_dict(only_annotated)
