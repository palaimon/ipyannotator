# ipyannotator - the infinitely hackable annotation framework

![CI-Badge](https://github.com/palaimon/ipyannotator/workflows/CI/badge.svg)


![jupytercon 2020](https://jupytercon.com/_nuxt/img/5035c8d.svg)


This is an pre-release version accompanying our [jupytercon 2020 talk](https://cfp.jupytercon.com/2020/schedule/presentation/237/ipyannotator-the-infinitely-hackable-annotation-framework/).
We hope this repository helps you to explore how annotation UI's can be quickly build
using only python code and leveraging many awesome libraries ([ipywidgets](https://github.com/jupyter-widgets/ipywidgets), [voila](https://github.com/voila-dashboards/voila), [ipycanvas](https://github.com/martinRenou/ipycanvas), etc.) from the [jupyter Eco-system](https://jupyter.org/).


At https://palaimon.io we have used the concepts underlying ipyannotator internally for various projects and
this is our attempt to contribute back to the OSS community some of the benefits we have had using OOS software.


## Please star, fork and open issues!


Please let us know if you find this repository useful. Your feedback will help us to turn this proof of concept into a comprehensive library.


## Install


`pip install ipyannotator`


**dependencies (should be handled by pip)**

```
python = "^3.7"
traitlets = '=4.3.3'
ipycanvas = "^0.5.1"
ipyevents = "^0.8.0"
ipywidgets = "^7.5.1"
```


## Run ipyannotator as stand-alone web app using voila

Dependency resolution fails if `nbdev` and `voila` libraries are both listed in the same `pyproject.toml`. This should be fixed in the next major release of `nbdev` lib. 

The easiest workaround atm:
 - install `ipyannotator` without dev dependencies 
 - manually install `voila` into the same dev environment

Using `poetry`:

install:
```shell
cd {project_root}
poetry install --no-dev
poetry run pip install voila
```
and run simple ipyannotator standalone example:
```shell 
poetry run voila nbs/09_viola_example.ipynb --enable_nbextensions=True
```

  
Same with `pip`:

```shell
   cd {project_root}
   
   pip install . 
   pip install voila
   
   voila nbs/09_viola_example.ipynb --enable_nbextensions=True
```
   

# Documentation

This library has been written in the [literate programming style](https://en.wikipedia.org/wiki/Literate_programming) popularized for
jupyter notebooks by [nbdev](https://www.fast.ai/2019/12/02/nbdev/). Please explore the jupyter notebooks in `nbs/` to learn more about
the inner working of ipyannotator.


Also check out the following notebook for a more high level overview.

- Tutorial demonstrating how ipyannotator can be seamlessly integrated in your
    data science workflow. `nbs/08_tutorial_road_damage.ipynb`
- Slides + recoding of jupytercon 2020 talk explaining the high level concepts / vision
    of ipyannotator. TODO add public link

## Jupyter lab trouble shooting

For clean (re)install make sure to have all the lab extencions active:

`jupyter lab clean` to remove the staging and static directories from the lab 

 _ipywidgets_:
 
 `jupyter labextension install @jupyter-widgets/jupyterlab-manager`
 
 _ipycanvas_:
 
 `jupyter labextension install @jupyter-widgets/jupyterlab-manager ipycanvas`
 
 _ipyevents_:
 
 `jupyter labextension install @jupyter-widgets/jupyterlab-manager ipyevents`
 
 _nbdime_:
 
 `nbdime extensions --enable [--sys-prefix/--user/--system]`
 
 _viola_:
 
 `jupyter labextension install @jupyter-voila/jupyterlab-preview`


# How to contribute


Check out `CONTRIBUTING.md` and since ipyannotator is build using nbdev reading
the [nbdev tutorial](https://nbdev.fast.ai/tutorial.html) and related docs will be very helpful.


## Copyright


Copyright 2020 onwards, Palaimon GmbH. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this project's files except in compliance with the License. A copy of the License is provided in the LICENSE file in this repository.

