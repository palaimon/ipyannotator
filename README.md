# Ipyannotator - the infinitely hackable annotation framework

![CI-Badge](https://github.com/palaimon/ipyannotator/workflows/CI/badge.svg)

Ipyannotator is a flexible annotation system. Developed to allow users to hack its features by extending and customizing it. 

The large variety of annotation tasks, data formats and data visualizations is a challenging when dealing with multiple domains of supervised machine learning (ML). The existent tooling is often not flexible enough which imposes limitations to the user. By providing a framework where users can use, customize and create their own annotation tooling this projects aims to solve this problem.

The library contains some pre-defined annotators that can be used out of the box, but it also can be extend and customized according to the users needs. Check our [tutorials](https://palaimon.github.io/ipyannotator/docs/tutorials.html) for a quickly understanding of it's usage and check our [API](https://palaimon.github.io/ipyannotator/nbs/21_api_doc.html) for quick reference.

This library has been written in the [literate programming style](https://en.wikipedia.org/wiki/Literate_programming) popularized for jupyter notebooks by [nbdev](https://www.fast.ai/2019/12/02/nbdev/). In addition to our [online documentation](palaimon.github.io/ipyannotator) the jupyter notebooks located at `nbs/` allow an interactive exploration of the inner workings of Ipyannotator.

We hope this repository helps you to explore how annotation UI's can be quickly built using only python code and leveraging many awesome libraries ([ipywidgets](https://github.com/jupyter-widgets/ipywidgets), [voila](https://github.com/voila-dashboards/voila), [ipycanvas](https://github.com/martinRenou/ipycanvas), etc.) from the [jupyter Eco-system](https://jupyter.org/).

At https://palaimon.io we have used the concepts underlying Ipyannotator internally for various projects and this is our attempt to contribute back to the OSS community some of the benefits we have had using OOS software.

## Please star, fork and open issues!

Please let us know if you find this repository useful. Your feedback will help us to turn this proof of concept into a comprehensive library.

## Install

Ipyannotator is available on Pypi and can be installed using:

`pip install ipyannotator`

## Running ipyannotator

Ipyannotator provides a [simple API](https://palaimon.github.io/ipyannotator/nbs/21_api_doc.html) that provides the ability to explore, create and improve annotation datasets by using a pair of input/outputs. All pair of input/output are [listed on Ipyannotator's docs](https://palaimon.github.io/ipyannotator/nbs/22_input_output_doc.html). Check [Ipyannotator tutorials](https://palaimon.github.io/ipyannotator/docs/tutorials.html) for a quickly demonstration of the library.

### Run ipyannotator tests

Ipyannotator's tests are directly integrated in the Jupyter Notebooks that make up the libraries source code, this is a consequence of following the literate programming style made possible by the library `nbdev`. Tests can be executed by running `nbdev_test_nbs` on the terminal.

When installing the repository using poetry, all dev dependencies are installed by default.

When using pip for installation make sure to install the two dev dependencies `pytest` and `ipytest`, with the versions listed in `pyproject.toml`, manually:

```shell
pip install pytest
pip install ipytest
```

[Nbdev](https://nbdev.fast.ai/#A-Motivating-Example) uses comments on the Jupyter notebook cells, such as `#exports`, to output the library code, and cells without comments to be executed as tests. Nbdev by itself doesn't guarantee that the tests are self-contained, that's why Ipyannotator uses [pytest](https://docs.pytest.org/en/7.1.x/) and [ipytest](https://github.com/chmp/ipytest) as dev dependencies.

### Run ipyannotator as stand-alone web app using voila

Ipyannotator can be executed as a web app using the [voila](https://github.com/voila-dashboards/voila) library. The following sections describe how to run using poetry and pip.

#### Using poetry

On your terminal:

```shell
cd {project_root}
poetry install --no-dev
```

Any jupyter notebook with ipyannotator can be executed as an standalone web application. An example of voila usage it's available in the current repository and can be executed as it follow:

```shell
poetry run voila nbs/09_voila_example.ipynb --enable_nbextensions=True
```

#### Using pip

The installation and execution process can also be done using pip.

```shell
   cd {project_root}
   
   pip install .
   pip install voila
   
   voila nbs/09_voila_example.ipynb --enable_nbextensions=True
```

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

## How to contribute

Check out `CONTRIBUTING.md` and since ipyannotator is build using nbdev reading
the [nbdev tutorial](https://nbdev.fast.ai/tutorial.html) and related docs will be very helpful.

## Additional resources

![jupytercon 2020](https://jupytercon.com/_nuxt/img/5035c8d.svg)

- [jupytercon 2020 talk](https://cfp.jupytercon.com/2020/schedule/presentation/237/ipyannotator-the-infinitely-hackable-annotation-framework/).

- [Recording of jupytercon 2020](https://www.youtube.com/watch?v=jFAp1s1O8Hg) talk explaining the high level concepts / vision of ipyannotator.

## Acknowledgements

The authors acknowledge the financial support by the Federal Ministry for Digital and Transport of Germany under the program mFUND (project number 19F2160A).

## Copyright

Copyright 2022 onwards, Palaimon GmbH. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this project's files except in compliance with the License. A copy of the License is provided in the LICENSE file in this repository.



<!-- Matomo Image Tracker-->
<img referrerpolicy="no-referrer-when-downgrade" src="https://matomo.palaimon.io/matomo.php?idsite=4&amp;rec=1" style="border:0" alt="" />
<!-- End Matomo -->
