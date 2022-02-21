# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_base.ipynb (unless otherwise specified).

__all__ = []

# Internal Cell

import json
import random
from pubsub import pub
from pathlib import Path
from typing import NamedTuple, Optional, Tuple, Any, Callable
from pydantic import BaseModel, BaseSettings

# Internal Cell

def validate_project_path(project_path):
    project_path = Path(project_path)
    assert project_path.exists(), "WARNING: Project path should point to " \
                                  "existing directory"
    assert project_path.is_dir(), "WARNING: Project path should point to " \
                                  "existing directory"
    return project_path

# Internal Cell

class Settings(NamedTuple):
    project_path: Path = Path('user_project')
    project_file: Optional[Path] = None
    image_dir: str = 'images'
    label_dir: Optional[str] = None
    result_dir: Optional[str] = None

    im_width: int = 50
    im_height: int = 50
    label_width: int = 50
    label_height: int = 50

    n_cols: int = 3
    n_rows: Optional[int] = None

# Internal Cell


def generate_subset_anno_json(project_path: Path, project_file,
                              number_of_labels,
                              out_filename='subset_anno.json'):
    """
    generates random subset from full dataset based on <number_of_labels>
    """
    if number_of_labels == -1:
        return project_file

    with project_file.open() as f:
        data = json.load(f)

    all_labels = data.values()
    unique_labels = set(label for item_labels in all_labels for label in item_labels)

    #  get <number_of_labels> random labels and generate annotation file with them:
    assert (number_of_labels <= len(unique_labels))
    subset_labels = random.sample([[a] for a in unique_labels], k=number_of_labels)
    subset_annotations = {k: v for k, v in data.items() if v in subset_labels}

    subset_file = Path(project_path) / out_filename
    with subset_file.open('w', encoding='utf-8') as fi:
        json.dump(subset_annotations, fi, ensure_ascii=False, indent=4)

    return subset_file

# Internal Cell

class StateSettings(BaseSettings):
    class Config:
        validate_assignment = True


class BaseState(StateSettings, BaseModel):
    def __init__(self, uuid: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_quietly('_uuid', uuid)

    def set_quietly(self, key: str, value: Any):
        """
        Assigns a value to a state's attribute.

        This function can be used to avoid that
        the state dispatches a PyPubSub event.
        It's very usefull to avoid event recursion,
        ex: a component is listening for an event A
        but it also changes the state that dispatch
        the event A. Using set_quietly to set the
        value at the component will avoid the recursion.
        """
        object.__setattr__(self, key, value)

    @property
    def root_topic(self) -> str:
        if hasattr(self, '_uuid') and self._uuid:  # type: ignore
            return f'{self._uuid}.{type(self).__name__}'  # type: ignore

        return type(self).__name__

    def subscribe(self, change: Callable, attribute: str):
        pub.subscribe(change, f'{self.root_topic}.{attribute}')

    def __setattr__(self, key: str, value: Any):
        self.set_quietly(key, value)

        if key != '__class__':
            pub.sendMessage(f'{self.root_topic}.{key}', **{key: value})

# Internal Cell

class AppWidgetState(BaseState):
    size: Tuple[int, int] = (640, 400)
    max_im_number: int = 1
    index: int = 0