# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/19_bbox_video_annotator.ipynb (unless otherwise specified).

__all__ = ['BBoxVideoAnnotator']

# Internal Cell
import attr
import warnings
from pubsub import pub
from attr import asdict
from copy import deepcopy
from typing import List, Dict, Optional
from itertools import groupby
from ipywidgets import HBox, VBox, Layout, Button, Checkbox, ToggleButton
from .bbox_canvas import BBoxVideoCanvas
from .base import AppWidgetState
from .right_menu_widget import BBoxVideoList, BBoxVideoItem
from .mltypes import BboxCoordinate, BboxVideoCoordinate
from .bbox_annotator import (
    BBoxAnnotator, BBoxState, BBoxAnnotatorController,
    BBoxAnnotatorGUI, BBoxCoordinates, BBoxCanvasState
)
from .services.bbox_trajectory import BBoxTrajectory

# Internal Cell

@attr.define
class BboxVideoCoordSelected:
    index: int
    frame: int
    bbox_video_coordinate: BboxVideoCoordinate

# Internal Cell

@attr.define
class BboxVideoHistory:
    label: List[str] = []
    trajectory: Dict[str, List[BboxCoordinate]] = {}
    bbox_coord: Optional[BboxVideoCoordinate] = None

# Internal Cell

class BBoxVideoState(BBoxState):
    trajectory: Dict[str, List[BboxCoordinate]] = {}
    drawing_trajectory_enabled: bool = True
    right_menu_enabled: bool = True
    bbox_coords_selected: List[BboxVideoCoordSelected] = []
    merged_trajectories: List[str] = []

# Internal Cell

class BBoxVideoCoordinates(BBoxCoordinates):
    """Connects the BBoxList and the states"""

    def __init__(
        self,
        app_state: AppWidgetState,
        bbox_canvas_state: BBoxCanvasState,
        bbox_state: BBoxVideoState,
        drawing_enabled: bool,
        on_btn_select_clicked: callable = None,
        on_label_changed: callable = None,
        on_trajectory_enabled_clicked=None,
    ):
        super().__init__(
            app_state,
            bbox_canvas_state,
            bbox_state,
            on_btn_select_clicked
        )

        self.trajectory_enabled_checkbox = Checkbox(
            description='Enable object tracking',
            value=self._bbox_state.drawing_trajectory_enabled
        )
        if on_trajectory_enabled_clicked:
            self.trajectory_enabled_checkbox.observe(on_trajectory_enabled_clicked, names='value')

        pub.unsubscribe(super()._sync_labels, f'{bbox_canvas_state.root_topic}.bbox_coords')
        pub.unsubscribe(super()._refresh_children, f'{app_state.root_topic}.index')

        self._bbox_list = BBoxVideoList(
            btn_delete_enabled=drawing_enabled,
            on_label_changed=on_label_changed,
            on_btn_delete_clicked=self.on_btn_delete_clicked,
            on_btn_select_clicked=on_btn_select_clicked,
            classes=bbox_state.classes,
            on_checkbox_object_clicked=self._on_checkbox_object_clicked
        )

        bbox_canvas_state.subscribe(self._update_max_coord_input, 'image_scale')

        self.children = self._bbox_list.children

    def __getitem__(self, index: int) -> BBoxVideoItem:
        return self.children[1][index]

    def _render(self, bbox_coords: List[BboxVideoCoordinate], labels: List[List[str]]):
        if self._bbox_state.right_menu_enabled:
            selected = []
            all_frame_object_ids = [bbox_coord.id for bbox_coord in self._bbox_state.coords]

            for coord in self._bbox_state.bbox_coords_selected:
                if coord.bbox_video_coordinate.id in all_frame_object_ids:
                    selected.append(coord.index)

            self._bbox_list.render_btn_list(
                bbox_coords=bbox_coords,
                classes=labels,
                labels=self._bbox_state.labels,
                selected=selected
            )
            self.children = VBox([
                self.trajectory_enabled_checkbox,
                self._bbox_list,
            ]).children

    def on_btn_delete_clicked(self, index: int):
        super().on_btn_delete_clicked(index)
        self._remove_object_selected(index)

    def _remove_object_selected(self, index: int):
        try:
            self._bbox_state.set_quietly(
                'bbox_coords_selected',
                list(filter(lambda x: x.index != index, self._bbox_state.bbox_coords_selected))
            )
        except Exception:
            warnings.warn("Couldn't unselect object")

    def _update_max_coord_input(self, image_scale: float):
        """CoordinateInput maximum values that a user
        can change. 'x' and 'y' can be improved to avoid
        bbox outside of the canvas area."""

        self._bbox_list.max_coord_input_values = {
            'x': self._app_state.size[0] / image_scale,
            'y': self._app_state.size[1] / image_scale,
            'width': self._app_state.size[0] / image_scale,
            'height': self._app_state.size[1] / image_scale
        }

    def _on_checkbox_object_clicked(self, change: dict, index: int,
                                    bbox_coord: BboxVideoCoordinate):
        if change['new']:
            self._bbox_state.bbox_coords_selected.append(
                BboxVideoCoordSelected(
                    frame=self._app_state.index,
                    index=index,
                    bbox_video_coordinate=bbox_coord
                )
            )
        else:
            self._remove_object_selected(index)

# Internal Cell

class BBoxAnnotatorVideoGUI(BBoxAnnotatorGUI):
    def __init__(
        self,
        on_label_changed: callable,
        on_join_btn_clicked: callable,
        on_bbox_drawn: callable,
        *args,
        drawing_enabled: bool = True,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.on_bbox_drawn = on_bbox_drawn
        self.bbox_trajectory = BBoxTrajectory()
        self.history = BboxVideoHistory()

        pub.unsubAll(f'{self._image_box.state.root_topic}.bbox_coords')

        self._image_box = BBoxVideoCanvas(
            *self._app_state.size,
            drawing_enabled=drawing_enabled
        )

        self.right_menu = BBoxVideoCoordinates(
            app_state=self._app_state,
            bbox_canvas_state=self._image_box.state,
            bbox_state=self._bbox_state,
            on_btn_select_clicked=self._highlight_bbox,
            on_label_changed=on_label_changed,
            drawing_enabled=drawing_enabled,
            on_trajectory_enabled_clicked=self.on_trajectory_enabled_clicked
        )

        self._navi.on_navi_clicked = self.view_idx_changed

        self.center = HBox(
            [self._image_box, self.right_menu],
            layout=Layout(
                display='flex',
                flex_flow='row'
            )
        )

        self._join_btn = Button(description="Join",
                                icon="compress",
                                layout=Layout(width='auto'))

        self._join_btn.on_click(on_join_btn_clicked)

        self.btn_right_menu_enabled = ToggleButton(
            description="Menu",
            tooltip="Disable right menu for a better navigation experience.",
            icon="eye-slash",
            disabled=False,
            value=not self._bbox_state.right_menu_enabled,
            layout=Layout(width="70px")
        )

        self.btn_right_menu_enabled.observe(
            self.on_right_menu_enabled_clicked,
            "value"
        )

        self.footer = HBox(
            [
                self._navi,
                self._save_btn,
                self._undo_btn,
                self._redo_btn,
                self._join_btn,
                self.btn_right_menu_enabled,
            ],
            layout=Layout(
                display='flex',
                flex_flow='row wrap',
                align_items='center'
            )
        )

        self._app_state.index = 0

        self._image_box.state.subscribe(self.render_right_menu, 'bbox_coords')
        if self._image_box.state.bbox_coords:
            self.render_right_menu(self._image_box.state.bbox_coords)

    def on_trajectory_enabled_clicked(self, change: dict):
        self._bbox_state.drawing_trajectory_enabled = not self._bbox_state.drawing_trajectory_enabled  # noqa: E501
        self._bbox_state.trajectory = {}
        self.refresh_gui()

    def on_right_menu_enabled_clicked(self, change: dict):
        menu_enabled = self._bbox_state.right_menu_enabled
        self._bbox_state.right_menu_enabled = not menu_enabled
        self.refresh_gui()

    def refresh_gui(self):
        self._image_box.clear_layer(-1)
        self.clear_right_menu()
        self.render_right_menu(self._image_box.state.bbox_coords)
        # refreshing bbox_coords on canvas
        self._image_box.state.bbox_coords = self._image_box.state.bbox_coords

    def render_right_menu(self, bbox_coords: List[BboxVideoCoordinate]):
        if self.on_bbox_drawn:
            self.on_bbox_drawn(bbox_coords)
            self.right_menu._render(bbox_coords, self._bbox_state.labels)
        if self._bbox_state.drawing_trajectory_enabled:
            self.draw_trajectory(bbox_coords)

    def clear_right_menu(self):
        self.right_menu._bbox_list.clear()
        self.right_menu.children = []

    def _redo_clicked(self, event: dict):
        if self.history.label is not None:
            self._bbox_state.labels.append(self.history.label)
            self.history.label = []
        if self.history.trajectory:
            for k, v in self.history.trajectory.items():
                self._bbox_state.trajectory[k] = v
            self.history.trajectory = {}
        if self.history.bbox_coord:
            tmp_bbox_coords = deepcopy(self._image_box.state.bbox_coords)
            tmp_bbox_coords.append(self.history.bbox_coord)
            self._image_box.state.bbox_coords = tmp_bbox_coords
            self.history.bbox_coord = None

    def _undo_clicked(self, event: dict):
        if self._bbox_state.labels:
            tmp_labels = deepcopy(self._bbox_state.labels)
            self.history.label = tmp_labels.pop()
            self._bbox_state.labels = tmp_labels

        tmp_bbox_coords = None
        if self._image_box.state.bbox_coords:
            tmp_bbox_coords = deepcopy(self._image_box.state.bbox_coords)
            self.history.bbox_coord = tmp_bbox_coords.pop()
            self._image_box.state.bbox_coords = tmp_bbox_coords

        if self.history.bbox_coord and self.history.bbox_coord.id in self._bbox_state.trajectory:
            tmp_trajectory = deepcopy(self._bbox_state.trajectory)
            self.history.trajectory = {
                self.history.bbox_coord.id: tmp_trajectory[self.history.bbox_coord.id]
            }
            del tmp_trajectory[self.history.bbox_coord.id]
            self._bbox_state.trajectory = tmp_trajectory
        self.refresh_gui()

    def view_idx_changed(self, index: int):
        # store the last bbox drawn before index update
        self._bbox_state.set_quietly(
            'coords',
            self._image_box._state.bbox_coords
        )
        self.clear_right_menu()
        self._app_state.index = index

    def draw_trajectory(self, bbox_coords: List[BboxVideoCoordinate]):
        """Draw trajectory checking if object lives on bbox canvas"""
        coords = self._bbox_video_to_trajectory(bbox_coords)
        coord_ids = [i.id for i in self._image_box.state.bbox_coords]
        for obj_id, value in coords.items():
            if len(value) > 1 and obj_id in coord_ids:
                self.bbox_trajectory.draw_trajectory(
                    self._image_box.multi_canvas[-1],
                    value,
                    self._image_box.state.image_scale
                )

    def _bbox_video_to_trajectory(
            self, coords: List[BboxVideoCoordinate]) -> Dict[str, List[BboxCoordinate]]:
        """Group objects and stores (in memory) a list of bbox coordinates"""
        def sort(k):
            return k['id']

        coords = [asdict(c) for c in coords]
        for k, v in groupby(sorted(coords, key=sort), sort):
            value = list(v)
            for i in value:
                bbox_coord = BboxCoordinate(*list(i.values())[:4])
                try:
                    if bbox_coord not in self._bbox_state.trajectory[k]:
                        self._bbox_state.trajectory[k].append(bbox_coord)
                except Exception:
                    self._bbox_state.trajectory[k] = [bbox_coord]

        return self._bbox_state.trajectory

# Internal Cell

class BBoxVideoAnnotatorController(BBoxAnnotatorController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _update_coords(self, index: int):  # from annotations
        image_path = str(self._storage.images[index])
        coords = self._storage.get(image_path) or {}
        self._bbox_state.labels = coords.get('labels', [])
        self._bbox_state.coords = [BboxVideoCoordinate(**c) for c in coords.get('bbox', [])]

    def _save_annotations(self, index: int, *args, **kwargs):
        image_path = str(self._storage.images[index])
        self._storage[image_path] = {
            'bbox': [asdict(bbox) for bbox in self._bbox_state.coords],
            'labels': self._bbox_state.labels,
        }
        self._storage.save()

    def update_storage_labels(self, change: dict, index: int):
        """Receive an object label update and updates all
        object's labels that share the same id"""
        self._bbox_state.labels[index] = [change['new']]
        bbox_coord_id = self._bbox_state.coords[index].id
        for image_path, bbox_or_labels in self._storage.items():
            if not bbox_or_labels or 'bbox' not in bbox_or_labels:
                break
            for i, bbox_coord in enumerate(bbox_or_labels['bbox']):
                if bbox_coord['id'] == bbox_coord_id:
                    self._storage[image_path]['labels'][i] = [change['new']]

    def update_storage_id(self, merged_ids: List[str]):
        """Update objects id's once one of them are merged.
        Returns the merged ids trajectory."""
        merge_id = "-".join(merged_ids)

        for image_path, bbox_or_labels in self._storage.items():
            if not bbox_or_labels or 'bbox' not in bbox_or_labels:
                break
            for bbox_coord in bbox_or_labels['bbox']:
                if bbox_coord['id'] in merged_ids:
                    bbox_coord['id'] = merge_id

    def _idx_changed(self, index: int):
        """
        On index change save an old state and update
        current image path and bbox coordinates for
        visualisation
        """
        self._save_annotations(self._last_index)
        self._update_im(index)
        self._update_coords(index)
        self._last_index = index

    def sync_labels(self, bbox_coords: List[BboxVideoCoordinate]):
        """Update labels according to the past frame labels
        or add an empty label to the bbox state. It also avoid to
        add empty labels if its length is the same as the bbox_coords"""
        num_classes = len(self._bbox_state.labels)

        for i, _ in enumerate(bbox_coords[num_classes:], num_classes):
            try:
                image_path = self._storage.images[self._app_state.index - 1]
                coords = self._storage.get(str(image_path)) or {}
                self._bbox_state.labels.append(
                    coords.get('labels')[i]
                )
            except Exception:
                self._bbox_state.labels.append([])

# Cell

class BBoxVideoAnnotator(BBoxAnnotator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **{**kwargs, 'render_previous_coords': False})
        pub.unsubscribe(self.controller._idx_changed, f'{self.app_state.root_topic}.index')
        pub.unsubAll(f'{self.app_state.root_topic}.index')
        state_params = {**self.bbox_state.dict()}
        state_params.pop('_uuid')
        self.bbox_state = BBoxVideoState(
            uuid=self.bbox_state._uuid,
            **state_params
        )

        self.controller = BBoxVideoAnnotatorController(
            app_state=self.app_state,
            bbox_state=self.bbox_state,
            storage=self.storage
        )

        self.view = BBoxAnnotatorVideoGUI(
            app_state=self.app_state,
            bbox_state=self.bbox_state,
            on_save_btn_clicked=self.on_save_btn_clicked,
            drawing_enabled=self._output_item.drawing_enabled,
            on_label_changed=self.update_labels,
            on_join_btn_clicked=self.merge_tracks_selected,
            on_bbox_drawn=self.controller.sync_labels
        )

    def update_labels(self, change: dict, index: int):
        """Saves bbox_canvas_state coordinates data
        on bbox_state and save all on storage."""
        self.bbox_state.set_quietly('coords', self.view._image_box._state.bbox_coords)
        self.controller.update_storage_labels(change, index)

    def on_save_btn_clicked(self, bbox_coords: List[dict]):
        self.controller.save_current_annotations(bbox_coords)

    def _update_state_id(self, merged_ids: List[str], bbox_coords: List[BboxVideoCoordinate]):
        merged_id = "-".join(merged_ids)

        for i, coord in enumerate(bbox_coords):
            if merged_id and bbox_coords[i].id in merged_ids:
                bbox_coords[i].id = merged_id

    def merge_tracks_selected(self, change: dict):
        selecteds = self.bbox_state.bbox_coords_selected

        if selecteds:
            merged_ids = [selected.bbox_video_coordinate.id for selected in selecteds]

            self._update_state_id(
                merged_ids=merged_ids,
                bbox_coords=self.view._image_box.state.bbox_coords
            )

            self.controller.update_storage_id(
                merged_ids=merged_ids
            )

            # merge trajectories
            key = "-".join(merged_ids)
            tmp_trajectory = self.bbox_state.trajectory.copy()
            for id, bbx in tmp_trajectory.items():
                if id in merged_ids:
                    try:
                        self.bbox_state.trajectory[key] += bbx
                    except Exception:
                        self.bbox_state.trajectory[key] = bbx

                    if id in self.bbox_state.trajectory:
                        # delete old trajectory id
                        del self.bbox_state.trajectory[id]

            # finished merge cleans selected bbox coords
            self.bbox_state.bbox_coords_selected = []

            self.view.clear_right_menu()
            self.view.render_right_menu(self.view._image_box.state.bbox_coords)